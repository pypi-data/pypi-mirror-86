""" Class to represent PhotoKit PHAsset instance """

# TODO: change all defaults to current version instead of original
# add original=False to export
# make burst/live methods get uuid from self instead of passing as arg

import pathlib
import threading

import AVFoundation
import CoreServices
import Foundation
import objc
import Photos
import Quartz


from .fileutil import FileUtil
from .utils import _get_os_version, get_preferred_uti_extension, increment_filename

# NOTE: This requires user have granted access to the terminal (e.g. Terminal.app or iTerm)
# to access Photos.  This should happen automatically the first time it's called. I've
# not figured out how to get the call to requestAuthorization_ to actually work in the case
# where Terminal doesn't automatically ask (e.g. if you use tcctutil to reset terminal priveleges)
# In the case where permission to use Photos was removed or reset, it looks like you also need
# to remove permission to for Full Disk Access then re-run the script in order for Photos to
# re-ask for permission

# pylint: disable=no-member
PHOTOS_VERSION_ORIGINAL = Photos.PHImageRequestOptionsVersionOriginal
PHOTOS_VERSION_UNADJUSTED = Photos.PHImageRequestOptionsVersionUnadjusted
PHOTOS_VERSION_CURRENT = Photos.PHImageRequestOptionsVersionCurrent


def NSURL_to_path(url):
    """ Convert NSURL to a path string """
    nsurl = Foundation.NSURL.alloc().initWithString_(
        Foundation.NSString.alloc().initWithString_(str(url))
    )
    return nsurl.fileSystemRepresentation().decode("utf-8")


class PhotoKitError(Exception):
    """Base class for exceptions in this module. """

    pass


class PhotoKitFetchFailed(PhotoKitError):
    """Exception raised for errors in the input. """

    pass


class PhotoKitAuthError(PhotoKitError):
    """Exception raised if unable to authorize use of PhotoKit. """

    pass


class PhotoKitExportError(PhotoKitError):
    """Exception raised if unable to export asset. """

    pass


class ImageData:
    """ Simple class to hold the data passed to the handler for 
        requestImageDataAndOrientationForAsset_options_resultHandler_ 
    """

    def __init__(self):
        self.metadata = None
        self.uti = None
        self.image_data = None
        self.info = None
        self.orientation = None


class AVAssetData:
    """ Simple class to hold the data passed to the handler for 
    """

    def __init__(self):
        self.asset = None
        self.export_session = None
        self.info = None
        self.audiomix = None


class LivePhotoData:
    """ Simple class to hold the data passed to the handler for 
        requestLivePhotoForAsset:targetSize:contentMode:options:resultHandler:
    """

    def __init__(self):
        self.result = None
        self.info = None


class PhotoAsset:
    """ PhotoKit PHAsset representation """

    def __init__(self, uuid):
        """ Return a PhotoAsset object for asset with UUID uuid
        
        Args:
            uuid: universally unique identifier for photo in the Photo library

        Raises:
            PhotoKitAuthError if unable to authorize access to PhotoKit
        """
        self.uuid = uuid

        # pylint: disable=no-member
        options = Photos.PHContentEditingInputRequestOptions.alloc().init()
        options.setNetworkAccessAllowed_(True)

        # check authorization status
        auth_status = self._authorize()
        if auth_status != Photos.PHAuthorizationStatusAuthorized:
            raise PhotoKitAuthError(
                f"Could not get authorizaton to use Photos: auth_status = {auth_status}"
            )

        # get image manager and request options
        self._manager = Photos.PHCachingImageManager.defaultManager()
        self._phasset = self._fetch(uuid)

    @property
    def phasset(self):
        """ Return PHAsset instance """
        return self._phasset

    @property
    def isphoto(self):
        """ Return True if asset is photo (image), otherwise False """
        return self.media_type == Photos.PHAssetMediaTypeImage

    @property
    def ismovie(self):
        """ Return True if asset is movie (video), otherwise False """
        return self.media_type == Photos.PHAssetMediaTypeVideo

    @property
    def isaudio(self):
        """ Return True if asset is audio, otherwise False """
        return self.media_type == Photos.PHAssetMediaTypeAudio

    @property
    def filename(self):
        """ Return original filename asset was imported with """
        resources = self._resources()
        for resource in resources:
            if (
                self.isphoto
                and resource.type() == Photos.PHAssetResourceTypePhoto
                or not self.isphoto
                and resource.type() == Photos.PHAssetResourceTypeVideo
            ):
                return resource.originalFilename()
        return None

    @property
    def hasadjustments(self):
        """ Check to see if a PHAsset has adjustment data associated with it
            Returns False if no adjustments, True if any adjustments """

        # reference: https://developer.apple.com/documentation/photokit/phassetresource/1623988-assetresourcesforasset?language=objc

        adjustment_resources = Photos.PHAssetResource.assetResourcesForAsset_(
            self.phasset
        )
        return any(
            (
                adjustment_resources.objectAtIndex_(idx).type()
                == Photos.PHAssetResourceTypeAdjustmentData
            )
            for idx in range(adjustment_resources.count())
        )

    @property
    def media_type(self):
        """ media type such as image or video """
        return self.phasset.mediaType()

    @property
    def media_subtypes(self):
        """ media subtype """
        return self.phasset.mediaSubtypes()

    @property
    def panorama(self):
        """ return True if asset is panorama, otherwise False """
        return self.media_subtypes == Photos.PHAssetMediaSubtypePhotoPanorama

    @property
    def hdr(self):
        """ return True if asset is HDR, otherwise False """
        return self.media_subtypes == Photos.PHAssetMediaSubtypePhotoHDR

    @property
    def screenshot(self):
        """ return True if asset is screenshot, otherwise False """
        return self.media_subtypes == Photos.PHAssetMediaSubtypePhotoScreenshot

    @property
    def live(self):
        """ return True if asset is live, otherwise False """
        return self.media_subtypes == Photos.PHAssetMediaSubtypePhotoLive

    @property
    def streamed(self):
        """ return True if asset is streamed video, otherwise False """
        return self.media_subtypes == Photos.PHAssetMediaSubtypeVideoStreamed

    @property
    def slow_mo(self):
        """ return True if asset is slow motion (high frame rate) video, otherwise False """
        return self.media_subtypes == Photos.PHAssetMediaSubtypeVideoHighFrameRate

    @property
    def time_lapse(self):
        """ return True if asset is time lapse video, otherwise False """
        return self.media_subtypes == Photos.PHAssetMediaSubtypeVideoTimelapse

    @property
    def portrait(self):
        """ return True if asset is portrait (depth effect), otherwise False """
        return self.media_subtypes == Photos.PHAssetMediaSubtypePhotoDepthEffect

    @property
    def burst(self):
        """ return burstIdentifier if image is burst otherwise False """
        burstID = self.phasset.burstIdentifier()
        return burstID or False

    @property
    def source_type(self):
        """ the means by which the asset entered the user's library """
        return self.phasset.sourceType()

    @property
    def pixel_width(self):
        """ width in pixels """
        return self.phasset.pixelWidth()

    @property
    def pixel_height(self):
        """ height in pixels """
        return self.phasset.pixelHeight()

    @property
    def date(self):
        """ date asset was created """
        return self.phasset.creationDate()

    @property
    def date_modified(self):
        """ date asset was modified """
        return self.phasset.modificationDate()

    @property
    def location(self):
        """ location of the asset """
        return self.phasset.location()

    @property
    def duration(self):
        """ duration of the asset """
        return self.phasset.duration()

    @property
    def favorite(self):
        """ True if asset is favorite, otherwise False """
        return self.phasset.isFavorite()

    @property
    def hidden(self):
        """ True if asset is hidden, otherwise False """
        return self.phasset.isHidden()

    def metadata(self, version=PHOTOS_VERSION_ORIGINAL):
        """ Return dict of asset metadata
        
        Args:
            version: which version of image (PHOTOS_VERSION_ORIGINAL or PHOTOS_VERSION_CURRENT); default is PHOTOS_VERSION_ORIGINAL
        """
        imagedata = self._request_image_data(version=version)
        return imagedata.metadata

    def uti(self, version=PHOTOS_VERSION_ORIGINAL):
        """ Return UTI of asset
        
        Args:
            version: which version of image (PHOTOS_VERSION_ORIGINAL or PHOTOS_VERSION_CURRENT); default is PHOTOS_VERSION_ORIGINAL
        """
        imagedata = self._request_image_data(version=version)
        return imagedata.uti

    def url(self, version=PHOTOS_VERSION_ORIGINAL):
        """ Return URL of asset
        
        Args:
            version: which version of image (PHOTOS_VERSION_ORIGINAL or PHOTOS_VERSION_CURRENT); default is PHOTOS_VERSION_ORIGINAL
        """
        imagedata = self._request_image_data(version=version)
        return str(imagedata.info["PHImageFileURLKey"])

    def path(self, version=PHOTOS_VERSION_ORIGINAL):
        """ Return path of asset
        
        Args:
            version: which version of image (PHOTOS_VERSION_ORIGINAL or PHOTOS_VERSION_CURRENT); default is PHOTOS_VERSION_ORIGINAL
        """
        imagedata = self._request_image_data(version=version)
        url = imagedata.info["PHImageFileURLKey"]
        return url.fileSystemRepresentation().decode("utf-8")

    def orientation(self, version=PHOTOS_VERSION_ORIGINAL):
        """ Return orientation of asset
        
        Args:
            version: which version of image (PHOTOS_VERSION_ORIGINAL or PHOTOS_VERSION_CURRENT); default is PHOTOS_VERSION_ORIGINAL
        """
        imagedata = self._request_image_data(version=version)
        return imagedata.orientation

    def degraded(self, version=PHOTOS_VERSION_ORIGINAL):
        """ Return True if asset is degraded version 
        
        Args:
            version: which version of image (PHOTOS_VERSION_ORIGINAL or PHOTOS_VERSION_CURRENT); default is PHOTOS_VERSION_ORIGINAL
        """
        imagedata = self._request_image_data(version=version)
        return imagedata.info["PHImageResultIsDegradedKey"]

    # TODO: doesn't work for videos
    # see https://stackoverflow.com/questions/26152396/how-to-access-nsdata-nsurl-of-slow-motion-videos-using-photokit
    # https://developer.apple.com/documentation/photokit/phimagemanager/1616935-requestavassetforvideo?language=objc
    # https://developer.apple.com/documentation/photokit/phimagemanager/1616981-requestexportsessionforvideo?language=objc
    # above 10.15 only
    def export(
        self, dest, filename=None, version=PHOTOS_VERSION_ORIGINAL, overwrite=False
    ):
        """ Export image to path

        Args:
            dest: str, path to destination directory
            filename: str, optional name of exported file; if not provided, defaults to asset's original filename
            version: which version of image (PHOTOS_VERSION_ORIGINAL or PHOTOS_VERSION_CURRENT); default is PHOTOS_VERSION_ORIGINAL
            overwrite: bool, if True, overwrites destination file if it already exists; default is False

        Returns:
            Path to exported image

        Raises:
            ValueError if dest is not a valid directory
        """

        # if self.live:
        #     raise NotImplementedError("Live photos not implemented yet")

        filename = pathlib.Path(filename) if filename else pathlib.Path(self.filename)

        dest = pathlib.Path(dest)
        if not dest.is_dir():
            raise ValueError("dest must be a valid directory: {dest}")

        output_file = None
        if self.isphoto:
            imagedata = self._request_image_data(version=version)
            ext = get_preferred_uti_extension(imagedata.uti)

            output_file = dest / f"{filename.stem}.{ext}"

            if not overwrite:
                output_file = pathlib.Path(increment_filename(output_file))

            with open(output_file, "wb") as fd:
                fd.write(imagedata.image_data)
        elif self.ismovie:
            videodata = self._request_video_data(version=version)
            if videodata.asset is None:
                raise PhotoKitExportError("Could not get video for asset")

            url = videodata.asset.URL()
            path = pathlib.Path(NSURL_to_path(url))
            if not path.is_file():
                raise FileNotFoundError("Could not get path to video file")
            ext = path.suffix
            output_file = dest / f"{filename.stem}{ext}"

            if not overwrite:
                output_file = pathlib.Path(increment_filename(output_file))

            FileUtil.copy(path, output_file)

        return str(output_file)

    def _authorize(self):
        (_, major, _) = _get_os_version()

        auth_status = 0
        if int(major) < 16:
            auth_status = Photos.PHPhotoLibrary.authorizationStatus()
            if auth_status != Photos.PHAuthorizationStatusAuthorized:
                # it seems the first try fails after Terminal prompts user for access so try again
                for _ in range(2):
                    Photos.PHPhotoLibrary.requestAuthorization_(self._auth_status)
                    auth_status = Photos.PHPhotoLibrary.authorizationStatus()
                    if auth_status == Photos.PHAuthorizationStatusAuthorized:
                        break
        else:
            # requestAuthorization deprecated in 10.16/11.0
            # but requestAuthorizationForAccessLevel not yet implemented in pyobjc (will be in ver 7.0)
            # https://developer.apple.com/documentation/photokit/phphotolibrary/3616053-requestauthorizationforaccesslev?language=objc
            auth_status = Photos.PHPhotoLibrary.authorizationStatus()
            if auth_status != Photos.PHAuthorizationStatusAuthorized:
                # it seems the first try fails after Terminal prompts user for access so try again
                for _ in range(2):
                    Photos.PHPhotoLibrary.requestAuthorization_(self._auth_status)
                    auth_status = Photos.PHPhotoLibrary.authorizationStatus()
                    if auth_status == Photos.PHAuthorizationStatusAuthorized:
                        break
        return auth_status

    def _fetch(self, uuid):
        """ fetch a PHAsset with uuid = uuid """

        # pylint: disable=no-member
        fetch_options = Photos.PHFetchOptions.alloc().init()
        fetch_result = Photos.PHAsset.fetchAssetsWithLocalIdentifiers_options_(
            [self.uuid], fetch_options
        )
        if fetch_result and fetch_result.count() == 1:
            return fetch_result.objectAtIndex_(0)
        else:
            raise PhotoKitFetchFailed(f"Fetch did not return result for uuid {uuid}")

    def _fetch_with_burst_id(self, burstid, all=False):
        """ fetch a PHAsset with uuid = uuid
        
        Args:
            burstid: str, burst ID
            all: return all burst assets; if False returns only those selected by the user

        Returns:
            list of PHAssets

        """

        # pylint: disable=no-member
        fetch_options = Photos.PHFetchOptions.alloc().init()
        fetch_options.setIncludeAllBurstAssets_(all)
        fetch_results = Photos.PHAsset.fetchAssetsWithBurstIdentifier_options_(
            burstid, fetch_options
        )
        if fetch_results and fetch_results.count() >= 1:
            return [
                fetch_results.objectAtIndex_(idx)
                for idx in range(fetch_results.count())
            ]
        else:
            raise PhotoKitFetchFailed(
                f"Fetch did not return result for burstid {burstid}"
            )

    def _request_image_data(self, version=PHOTOS_VERSION_ORIGINAL):
        """ Request image data and metadata for self._phasset 
            
        Args:
            version: which version to request
                     PHOTOS_VERSION_ORIGINAL (default), request original highest fidelity version 
                     PHOTOS_VERSION_CURRENT, request current version with all edits
                     PHOTOS_VERSION_UNADJUSTED, request highest quality unadjusted version
        
        Raises:
            ValueError if passed invalid value for version
        """

        # reference: https://developer.apple.com/documentation/photokit/phimagemanager/3237282-requestimagedataandorientationfo?language=objc

        if version not in [
            PHOTOS_VERSION_CURRENT,
            PHOTOS_VERSION_ORIGINAL,
            PHOTOS_VERSION_UNADJUSTED,
        ]:
            raise ValueError("Invalid value for version")

        # pylint: disable=no-member
        options_request = Photos.PHImageRequestOptions.alloc().init()
        options_request.setNetworkAccessAllowed_(True)
        options_request.setSynchronous_(True)
        options_request.setVersion_(version)
        options_request.setDeliveryMode_(
            Photos.PHImageRequestOptionsDeliveryModeHighQualityFormat
        )
        requestdata = ImageData()
        handler, event = self._make_result_handle(requestdata)
        self._manager.requestImageDataAndOrientationForAsset_options_resultHandler_(
            self.phasset, options_request, handler
        )
        event.wait()
        self._imagedata = requestdata
        return requestdata

    def _request_video_data(self, version=PHOTOS_VERSION_ORIGINAL):
        """ Request video data for self._phasset 
            
        Args:
            version: which version to request
                     PHOTOS_VERSION_ORIGINAL (default), request original highest fidelity version 
                     PHOTOS_VERSION_CURRENT, request current version with all edits
                     PHOTOS_VERSION_UNADJUSTED, request highest quality unadjusted version
        
        Raises:
            ValueError if passed invalid value for version
        """

        if version not in [
            PHOTOS_VERSION_CURRENT,
            PHOTOS_VERSION_ORIGINAL,
            PHOTOS_VERSION_UNADJUSTED,
        ]:
            raise ValueError("Invalid value for version")

        options_request = Photos.PHVideoRequestOptions.alloc().init()
        options_request.setNetworkAccessAllowed_(True)
        options_request.setVersion_(version)
        options_request.setDeliveryMode_(
            Photos.PHVideoRequestOptionsDeliveryModeHighQualityFormat
        )
        requestdata = AVAssetData()
        handler, event = self._make_video_request_handle(requestdata)
        self._manager.requestAVAssetForVideo_options_resultHandler_(
            self.phasset, options_request, handler
        )
        event.wait()
        return requestdata

    # TODO: this doesn't work
    # https://www.iditect.com/how-to/50021893.html
    # https://stackoverflow.com/questions/41224006/how-to-get-video-from-a-live-photo-in-ios
    def _request_live_photo_data(self, version=PHOTOS_VERSION_ORIGINAL):
        """ get live photo data """
        # reference https://developer.apple.com/documentation/photokit/phimagemanager/1616984-requestlivephotoforasset?language=objc

        if version not in [
            PHOTOS_VERSION_CURRENT,
            PHOTOS_VERSION_ORIGINAL,
            PHOTOS_VERSION_UNADJUSTED,
        ]:
            raise ValueError("Invalid value for version")

        options_request = Photos.PHLivePhotoRequestOptions.alloc().init()
        options_request.setNetworkAccessAllowed_(True)
        options_request.setVersion_(version)
        # options_request.setIsSynchronous_(True)
        options_request.setDeliveryMode_(
            Photos.PHImageRequestOptionsDeliveryModeOpportunistic
            # Photos.PHVideoRequestOptionsDeliveryModeHighQualityFormat
        )

        size = Quartz.CGSize(width=self.pixel_width, height=self.pixel_height)
        requestdata = LivePhotoData()
        # handler, event = self._make_live_photo_request_handle(requestdata)
        # handler, event = self._make_live_photo_request_handle(requestdata)

        # import libdispatch

        # request_queue = libdispatch.dispatch_queue_create(b"Request Queue", None)
        # semaphore = libdispatch.dispatch_semaphore_create(0)

        # event = threading.Event()

        # import libdispatch

        # queue = libdispatch.dispatch_queue_create(b"Image Queue", None)

        # def progress(progress, error, stop, info):
        #     print(f"progress: {progress}, info: {info}")
        #     import os

        #     os.system("say progress")

        # options_request.setProgressHandler_(progress)

        # sem = libdispatch.dispatch_semaphore_create(0)

        # event = threading.Event()
        def completion(livephoto):
            # print(f"I got a live photo!: {livephoto}")
            event.set()
            # libdispatch.dispatch_semaphore_signal(sem)

        # from PyObjCTools import AppHelper
        def handler(result, info):
            """ result handler for requestLivePhotoForAsset:targetSize:contentMode:options:resultHandler: """
            # event.set()
            nonlocal requestdata

            requestdata.result = result
            requestdata.info = info
            # completion(result)
            # libdispatch.dispatch_semaphore_signal(semaphore)

        self._manager.requestLivePhotoForAsset_targetSize_contentMode_options_resultHandler_(
            self.phasset,
            # size,
            Photos.PHImageManagerMaximumSize,
            Photos.PHImageContentModeDefault,
            options_request,
            handler,
        )
        # AppHelper.runConsoleEventLoop()

        # event.wait(60)
        # import time

        # libdispatch.dispatch_async(queue, get_live_photo)
        # time.sleep(1)
        # libdispatch.dispatch_semaphore_wait(sem, libdispatch.DISPATCH_TIME_FOREVER)
        # print(f"pid = {pid}")

        # event.wait(10)
        # libdispatch.dispatch_async(request_queue, get_live)
        # get_live()
        return requestdata

    def _auth_status(self, status):
        """ Handler for requestAuthorization_ """
        # This doesn't actually get called but requestAuthorization needs a callable handler
        # The Terminal will handle the actual authorization when called
        pass

    def _make_result_handle(self, data):
        """ Make handler function and threading event to use with 
            requestImageDataAndOrientationForAsset_options_resultHandler_ 
            data: Fetchdata class to hold resulting metadata 
            returns: handler function, threading.Event() instance 
            Following call to requestImageDataAndOrientationForAsset_options_resultHandler_, 
            data will hold data from the fetch """

        event = threading.Event()

        def handler(imageData, dataUTI, orientation, info):
            """ result handler for requestImageDataAndOrientationForAsset_options_resultHandler_ 
                all returned by the request is set as properties of nonlocal data (Fetchdata object) """

            nonlocal data

            options = {}
            # pylint: disable=no-member
            options[Quartz.kCGImageSourceShouldCache] = Foundation.kCFBooleanFalse
            imgSrc = Quartz.CGImageSourceCreateWithData(imageData, options)
            data.metadata = Quartz.CGImageSourceCopyPropertiesAtIndex(
                imgSrc, 0, options
            )
            data.uti = dataUTI
            data.orientation = orientation
            data.info = info
            data.image_data = imageData

            event.set()

        return handler, event

    def _make_video_request_handle(self, data):
        """ Make handler function and threading event to use with 
            requestAVAssetForVideo:asset options:options resultHandler

        Args:
            data: Fetchdata class to hold resulting data 

            returns: handler function and threading.Event() instance
        """

        event = threading.Event()

        def handler(asset, audiomix, info):
            """ result handler for requestAVAssetForVideo:asset options:options resultHandler """
            nonlocal data

            data.asset = asset
            data.audiomix = audiomix
            data.info = info

            event.set()

        return handler, event

    def _make_live_photo_request_handle(self, data):
        """ Make handler function and threading event to use with 
            requestAVAssetForVideo:asset options:options resultHandler

        Args:
            data: Fetchdata class to hold resulting data 

            returns: handler function and threading.Event() instance
        """

        event = threading.Event()
        should_return = True

        def completion(livephoto):
            print(f"I got a live photo!: {livephoto}")

        def handler(result, info):
            """ result handler for requestLivePhotoForAsset:targetSize:contentMode:options:resultHandler: """
            # nonlocal data
            nonlocal should_return

            if not should_return:
                return

            # # if should_return:
            # data.result = result
            # data.info = info

            if result:
                should_return = False
                completion(result)
                event.set()
            # else:
            #     completion(None)

            # should_return = False
            # event.set()

        # return handler, event
        return handler, event

    def _resources(self):
        """ Return list of PHAssetResource for object """
        resources = Photos.PHAssetResource.assetResourcesForAsset_(self.phasset)
        return [resources.objectAtIndex_(idx) for idx in range(resources.count())]
