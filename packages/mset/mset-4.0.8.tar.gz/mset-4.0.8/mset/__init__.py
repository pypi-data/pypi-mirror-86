def bakeAll(frame):
	"""
	Bakes all objects in the scene.
	"""
	pass

def compressFile(filePath, archiveOutputPath):
	"""
	Compresses a file on disk into a gzipped tarball archive (tgz).
	"""
	pass

def compressFolder(folderPath, archiveOutputPath):
	"""
	Compresses a folder, including all subdirectories, into a gzipped tarball archive (tgz).
	"""
	pass

def err(string):
	"""
	Prints text to the application log, as an error. No return will be appended.
	"""
	pass

def exportGLTF(path='', quality=3, metalnessThreshold=0.8):
	"""
	Exports a WebGL-ready glTF (.glb) archive. This file will be written to the file path specified, or to the scene's default location if no path is specified. Texture quality is set from 0 to 4, with 4 being the highest. The specular metalness conversion threshold is a value above which materials will be converted to metalness.
	"""
	pass

def exportViewer(path='', html=False):
	"""
	Exports a Marmoset Viewer (.mview) archive. This file will be written to the file path specified, or to the scene's default location if no path is specified.
	"""
	pass

def fail(message):
	"""
	Generates a failure message to an automated testing log. Mainly for internal use.
	"""
	pass

def findMaterial(name):
	"""
	Finds a Material by string name.
	"""
	pass

def findObject(searchString):
	"""
	Finds an Object in the scene by string name.
	"""
	pass

def frameObject(object):
	"""
	Centers and frames the given object in the current camera.
	"""
	pass

def frameScene():
	"""
	Centers and frames the entire scene in the current camera.
	"""
	pass

def freeUnusedResources():
	"""
	Frees from memory any retained but unused resources (such as textures). Generally this function is unnecessary, but it can be useful to keep total memory use lower in scripts that batch process large numbers of resources. Called automatically whenever a new scene is created or loaded.
	"""
	pass

def getAllMaterials():
	"""
	Returns all materials as a list.
	"""
	pass

def getAllObjects():
	"""
	Returns all scene Objects as a list.
	"""
	pass

def getPluginPath():
	"""
	Returns the current plugin path (eg. "C:/Program Files/Marmoset Toolbag 4/data/plugins/Example.py").
	"""
	pass

def getScenePath():
	"""
	Returns the path of the current scene file.
	"""
	pass

def getSceneUnitScale():
	"""
	Returns the current unit size of the scene, in meters. For example, a scene working in centimeters will return 0.01.
	"""
	pass

def getSelectedMaterial():
	"""
	Returns the currently selected Material.
	"""
	pass

def getSelectedMaterialGroup():
	"""
	Returns the currently selected Material group as an array of materials.
	"""
	pass

def getSelectedObject():
	"""
	Returns the currently selected Object. If multiple objects are selected this function will return the first selection. See also 'getSelectedObjects'.
	"""
	pass

def getSelectedObjects():
	"""
	Returns all currently selected scene Objects as a list.
	"""
	pass

def getTimeline():
	"""
	Returns the current scene's timeline, for animation control.
	"""
	pass

def getToolbagVersion():
	"""
	Returns the current toolbag version, as an integer (e.g. 4007).
	"""
	pass

def groupObjects(list):
	"""
	Groups an array of SceneObjects.
	"""
	pass

def importMaterial(filePath, name=''):
	"""
	Imports the specified material file into the scene. If no name is given, one will be automatically assigned.This function supports import from Toolbag materials, MTL files, Valve/Dota materials, and named texture files.Returns the imported material.
	"""
	pass

def importModel(filePath):
	"""
	Imports the specified model into the existing scene, using the scene's current import settings.Returns the imported object.
	"""
	pass

def loadScene(filePath):
	"""
	Loads a Marmoset Toolbag scene file.Unsaved changes to any currently open scenes are lost.
	"""
	pass

def log(string):
	"""
	Prints text to the application log. No return will be appended.You may wish to use python's print() method instead.
	"""
	pass

def newScene():
	"""
	Creates a new empty scene.Any unsaved changes in the current scene will be lost.
	"""
	pass

def quit():
	"""
	Quits the application. Any unsaved changes will be lost.
	"""
	pass

def readAndExportStamp(inputPath, outputPath):
	"""
	Marmoset internal use for stamp brush creation
	"""
	pass

def renderCamera(path='', width=-1, height=-1, sampling=-1, transparency=False, camera=''):
	"""
	Renders an image with the given camera, or the main camera if none is specified. This will use the current resolution/format settings from the render scene object. Returns an mset.Image instance. Optionally takes a path parameter, which specifies where to write the image. If no path is specified, no image file will be written.
	"""
	pass

def renderImages(width=-1, height=-1, sampling=-1, transparency=False):
	"""
	Renders images with the render scene object's current settings and cameras. To render a single image, see renderCamera().
	"""
	pass

def renderVideos(width=-1, height=-1, sampling=-1, transparency=False):
	"""
	Captures an animation into a video file or image sequence. The animation will be written into the file path(s) specified in the scene's render object.
	"""
	pass

def saveScene(filePath):
	"""
	Saves a Marmoset Toolbag scene file.If a scene file path is not specified, the scene will be saved to its existing location.
	"""
	pass

def setCamera(camera):
	"""
	Sets the current active camera for viewport and screenshot rendering.
	"""
	pass

def showOkCancelDialog(title, prompt):
	"""
	Prompts the user with a modal dialog box. The window is given a titlebar named 'title' and prompt text 'prompt'. Returns True or False depending on whether OK or Cancel is selected.
	"""
	pass

def showOpenFileDialog(...):
	"""
	Prompts the user with a file open dialog box, and resumes after the user selects a file.Returns the selected file path, or an empty string if the user canceled the dialog.Permitted file extensions can be optionally specified by the fileTypes array, which can contain one or more of: 'images', 'models', 'materials', which specify categories of file types, individual file extensions supported by Marmoset Toolbag (such as 'jpg', 'fbx', etc.), or at most one custom file extension. Specify extension names in lower case without the '.' character.Multiple files my be selected, and paths will be returned as an array, if 'multiple' is set to True.
	"""
	pass

def showOpenFolderDialog():
	"""
	Prompts the user with a folder open dialog box, and resumes after the user selects a folder.Returns the selected file path, or an empty string if the user canceled the dialog.
	"""
	pass

def showSaveFileDialog(fileTypes=[]):
	"""
	Prompts the user with a file save dialog box, and resumes after the user selects a file destination.Returns the selected file path, or an empty string if the user canceled the dialog.Permitted file extensions can be optionally specified by the fileTypes array, which can contain one or more of: 'images', 'models', 'materials', which specify categories of file types, individual file extensions supported by Marmoset Toolbag (such as 'jpg', 'fbx', etc.), or at most one custom file extension. Specify extension names in lower case without the '.' character.
	"""
	pass

def shutdownPlugin():
	"""
	Halts execution and shuts down the currently running plugin.
	"""
	pass

class AOBakerMap:
	"""
	Bent Normal Baker Map Settings
	"""
	
	cosineWeight = None
	"""Weights from -1 to 1, increasing values result in more 'cavity' shadows."""
	
	dither = None
	"""Determines whether this map output will be dithered."""
	
	enabled = None
	"""Whether or not this Baker Map should render when baking."""
	
	floor = None
	"""The amount of floor occlusion."""
	
	floorOcclusion = None
	"""Determines whether an artificial floor plane will be used for ambient occlusion baking."""
	
	ignoreGroups = None
	"""Determines whether bake groups will be ignored when baking ambient occlusion."""
	
	rayCount = None
	"""The number of rays used for AO baking."""
	
	searchDistance = None
	"""The maximum distance rays can go. 0 defaults to infinity."""
	
	suffix = None
	"""The output suffix of the current Baker Map."""
	
	twoSided = None
	"""Determines whether the ambient occlusion baking will also use back faces."""
	
	def resetSuffix():
		"""
		Resets the current map suffix to its default.
		"""
		pass

class BackdropObject:
	"""
	Backdrop Object
	"""
	
	alpha = None
	"""The transparency of the backdrop image."""
	
	collapsed = None
	"""Controls the display of the object's children in the outline view."""
	
	locked = None
	"""Controls the locking of object settings in the user interface."""
	
	name = None
	"""The name of the object."""
	
	parent = None
	"""The parent of the object."""
	
	path = None
	"""The file path to the backdrop image."""
	
	useAlpha = None
	"""Specifies whether or not to use the image's alpha channel."""
	
	visible = None
	"""Controls object viewport visibility."""
	
	def destroy():
		"""
		Destroys the object and removes it from the scene.
		"""
		pass
	def duplicate(name=''):
		"""
		Duplicates the object, optionally assigning it a new name. Returns the new object.
		"""
		pass
	def findInChildren(searchStr):
		"""
		Finds and returns an object with a name matching 'searchStr', parented under this object. The search recursively checks all child objects.
		"""
		pass
	def getChildren():
		"""
		Returns a list of all immediate children of the object.
		"""
		pass
	def setKeyframe(lerp):
		"""
		Sets a keyframe on this object with the assigned interpolation function ("linear", "spline", or "splineBreak"). This setting defaults to editor's default.
		"""
		pass

class BakerMap:
	"""
	Baker Map Settings
	"""
	
	enabled = None
	"""Whether or not this Baker Map should render when baking."""
	
	suffix = None
	"""The output suffix of the current Baker Map."""
	
	def resetSuffix():
		"""
		Resets the current map suffix to its default.
		"""
		pass

class BakerObject:
	"""
	Baker Object
	"""
	
	collapsed = None
	"""Controls the display of the object's children in the outline view."""
	
	edgePadding = None
	"""Edge padding amount. Must be one of the following values: 'None', 'Moderate', 'Extreme'."""
	
	edgePaddingSize = None
	"""Edge padding size in pixels."""
	
	fixMirroredTangents = None
	"""Fixes mirrored tangents, use this setting if you're seeing artifacts in your normal map bakes from your tangent space."""
	
	ignoreBackfaces = None
	"""Determines whether back sides of faces will be ignored when baking."""
	
	ignoreTransforms = None
	"""Determines whether transforms on meshes will be used when baking."""
	
	locked = None
	"""Controls the locking of object settings in the user interface."""
	
	multipleTextureSets = None
	"""Enables the use of Texture Sets when baking."""
	
	name = None
	"""The name of the object."""
	
	outputBits = None
	"""Bit depth of the output format; must be one of the following values: 8, 16, 32."""
	
	outputHeight = None
	"""The height in pixels of the baked textures."""
	
	outputPath = None
	"""The file path where the baked textures will be stored."""
	
	outputSamples = None
	"""Sample count of the bake output; must be one of the following values: 1, 4, 16."""
	
	outputSinglePsd = None
	"""Determines whether the baked maps will be stored inside a single PSD file, or multiple files."""
	
	outputSoften = None
	"""Determines how much the baked result will be softened; must be between 0.0 and 1.0."""
	
	outputWidth = None
	"""The width in pixels of the baked textures."""
	
	parent = None
	"""The parent of the object."""
	
	smoothCage = None
	"""Determines whether the cage mesh will use smooth vertex normals, ignoring any hard edges."""
	
	useHiddenMeshes = None
	"""Determines whether hidden meshes will be used when baking."""
	
	visible = None
	"""Controls object viewport visibility."""
	
	def addGroup(name):
		"""
		Adds a BakeGroup to the BakerObject.name: The Name of the BakeGroupreturns: The BakeGroup
		"""
		pass
	def bake():
		"""
		Bakes with the current configuration.
		"""
		pass
	def destroy():
		"""
		Destroys the object and removes it from the scene.
		"""
		pass
	def duplicate(name=''):
		"""
		Duplicates the object, optionally assigning it a new name. Returns the new object.
		"""
		pass
	def findInChildren(searchStr):
		"""
		Finds and returns an object with a name matching 'searchStr', parented under this object. The search recursively checks all child objects.
		"""
		pass
	def getAllMaps():
		"""
		Gets a list of all baker maps.returns: A list of all baker map handles
		"""
		pass
	def getChildren():
		"""
		Returns a list of all immediate children of the object.
		"""
		pass
	def getMap(name):
		"""
		Gets a baker map handle.name: The Name of the Map you wantreturns: A handle to the Baker Output Map
		"""
		pass
	def getTextureSetCount():
		"""
		Gets the number of texture sets in the current BakerObject.returns: integer number of texture sets.
		"""
		pass
	def getTextureSetEnabled(i):
		"""
		Gets the enabled status of a texture set.i: The index of the texture set you wantreturns: True if the texture set is enabled False if not.
		"""
		pass
	def getTextureSetHeight(i):
		"""
		Gets the height of a texture set.i: The index of the texture set you wantreturns: Height of the texture set.
		"""
		pass
	def getTextureSetName(i):
		"""
		Gets the name of a given texture set.i: The index of the Texture Set you wantreturns: the string name of the texture set.
		"""
		pass
	def getTextureSetWidth(i):
		"""
		Gets the width of a texture set.i: The index of the texture set you wantreturns: Width of texture set.
		"""
		pass
	def importModel(path):
		"""
		Imports a model file via the Baker's quick loader.path: string path to model file
		"""
		pass
	def loadPreset(name):
		"""
		loads a given preset for the BakerObject.name: The Name of the Preset
		"""
		pass
	def savePreset(name):
		"""
		saves the current configuration of the BakerObject.name: The Name of the Preset
		"""
		pass
	def setKeyframe(lerp):
		"""
		Sets a keyframe on this object with the assigned interpolation function ("linear", "spline", or "splineBreak"). This setting defaults to editor's default.
		"""
		pass
	def setTextureSetEnabled(i, enabled):
		"""
		Sets whether or the texture set specified is enabled or disabled.i: The index of the Texture Set you wantenabled: if the texture set should bake or not.
		"""
		pass
	def setTextureSetHeight(i, height):
		"""
		Sets the height of a given texture set.i: The index of the Texture Set you wantheight: your desired height of the texture set.
		"""
		pass
	def setTextureSetWidth(i, width):
		"""
		Sets the width of a given texture set.i: The index of the Texture Set you wantwidth: your desired width of the texture set.
		"""
		pass

class BakerTargetObject:
	"""
	Baker Target Object
	"""
	
	cageAlpha = None
	"""The opacity of the cage."""
	
	collapsed = None
	"""Controls the display of the object's children in the outline view."""
	
	excludeWhenIgnoringGroups = None
	"""Whether this target will be used when ignoring groups in cone based ray passes (AO, Bent Normals)."""
	
	locked = None
	"""Controls the locking of object settings in the user interface."""
	
	maxOffset = None
	"""The maximum offset of the cage mask."""
	
	minOffset = None
	"""The minimum offset of the cage mask."""
	
	name = None
	"""The name of the object."""
	
	parent = None
	"""The parent of the object."""
	
	visible = None
	"""Controls object viewport visibility."""
	
	def destroy():
		"""
		Destroys the object and removes it from the scene.
		"""
		pass
	def duplicate(name=''):
		"""
		Duplicates the object, optionally assigning it a new name. Returns the new object.
		"""
		pass
	def estimateOffset():
		"""
		Estimates the Cage Offsets.
		"""
		pass
	def findInChildren(searchStr):
		"""
		Finds and returns an object with a name matching 'searchStr', parented under this object. The search recursively checks all child objects.
		"""
		pass
	def getChildren():
		"""
		Returns a list of all immediate children of the object.
		"""
		pass
	def setKeyframe(lerp):
		"""
		Sets a keyframe on this object with the assigned interpolation function ("linear", "spline", or "splineBreak"). This setting defaults to editor's default.
		"""
		pass

class BentNormalBakerMap:
	"""
	Bent Normal Baker Map Settings
	"""
	
	dither = None
	"""Determines whether this map output will be dithered."""
	
	enabled = None
	"""Whether or not this Baker Map should render when baking."""
	
	flipX = None
	"""Determines whether the normal map's X channel will be flipped."""
	
	flipY = None
	"""Determines whether the normal map's Y channel will be flipped."""
	
	flipZ = None
	"""Determines whether the normal map's Z channel will be flipped."""
	
	ignoreGroups = None
	"""Determines whether bake groups will be ignored when baking bent normals."""
	
	rayCount = None
	"""The number of rays used for Bent Normal baking."""
	
	searchDistance = None
	"""The maximum distance rays can go. 0 defaults to infinity."""
	
	suffix = None
	"""The output suffix of the current Baker Map."""
	
	def resetSuffix():
		"""
		Resets the current map suffix to its default.
		"""
		pass

class Callbacks:
	"""
	Callbacks
	"""
	
	onPeriodicUpdate = None
	"""This Callback will run periodically: a few times per second. This can be useful for plugins that need to refresh external files or make frequent polling checks. Since this callback is run frequently, care should be taken to keep the average execution time low, or poor performance could result."""
	
	onRegainFocus = None
	"""This Callback will run when the application regains focus. This can be useful for plugins that need to refresh files or make other checks when the user switches to Toolbag."""
	
	onSceneChanged = None
	"""This Callback will run when the scene is changed (e.g. by moving an object)."""
	
	onSceneLoaded = None
	"""This Callback will run when a new scene is loaded."""
	
	onShutdownPlugin = None
	"""This Callback will run immediately before the plugin is shut down."""
	

class CameraObject:
	"""
	Camera Object
	"""
	
	collapsed = None
	"""Controls the display of the object's children in the outline view."""
	
	focalLength = None
	"""The focal length of the camera, in mm."""
	
	fov = None
	"""The vertical field of view of the camera, in degrees."""
	
	locked = None
	"""Controls the locking of object settings in the user interface."""
	
	name = None
	"""The name of the object."""
	
	nearPlaneScale = None
	"""A scalar for adjusting the automatic near clipping plane. Lower values will bring the clipping closer to the camera, but can result in unstable depth for the rest of the scene."""
	
	parent = None
	"""The parent of the object."""
	
	position = None
	"""The position of the object, as a list of 3 floats."""
	
	rotation = None
	"""The rotation of the object, as a list of 3 floats."""
	
	scale = None
	"""The scale of the object, as a list of 3 floats."""
	
	visible = None
	"""Controls object viewport visibility."""
	
	def destroy():
		"""
		Destroys the object and removes it from the scene.
		"""
		pass
	def duplicate(name=''):
		"""
		Duplicates the object, optionally assigning it a new name. Returns the new object.
		"""
		pass
	def findInChildren(searchStr):
		"""
		Finds and returns an object with a name matching 'searchStr', parented under this object. The search recursively checks all child objects.
		"""
		pass
	def getChildren():
		"""
		Returns a list of all immediate children of the object.
		"""
		pass
	def getLens():
		"""
		Returns a CameraLens object containing the camera lens settings. In order to set the camera lens, use setLens().
		"""
		pass
	def getLimits():
		"""
		Returns a CameraLimits object containing the camera limits settings. In order to set the camera limits, use setLimits().
		"""
		pass
	def getPostEffect():
		"""
		Returns a CameraPostEffect object containing the camera post effect settings. In order to set the camera post effect, use setPostEffect()
		"""
		pass
	def loadPostEffect(path):
		"""
		Load a camera post effect from a file.
		"""
		pass
	def savePostEffect(path):
		"""
		Save a camera post effect to a file.
		"""
		pass
	def setKeyframe(lerp):
		"""
		Sets a keyframe on this object with the assigned interpolation function ("linear", "spline", or "splineBreak"). This setting defaults to editor's default.
		"""
		pass
	def setLens(lens):
		"""
		Sets the camera lens from a CameraLens object. In order to retrieve the camera lens, use getLens().
		"""
		pass
	def setLimits(limits):
		"""
		Sets the camera limits from a CameraLimits object. In order to retrieve the camera limits, use getLimits().
		"""
		pass
	def setPostEffect(postEffect):
		"""
		Sets the camera post effect from a CameraPostEffect object. In order to retrieve the camera post effect, use getPostEffect().
		"""
		pass

class CameraObject.CameraLens:
	"""
	Camera Lens Settings
	"""
	
	distortionBarrel = None
	"""Strength of the barrel distortion effect."""
	
	distortionCABlue = None
	"""Strength of the chromatic aberration in the blue component."""
	
	distortionCAGreen = None
	"""Strength of the chromatic aberration in the green component."""
	
	distortionCARed = None
	"""Strength of the chromatic aberration in the red component."""
	
	distortionChromaticAberration = None
	"""Strength of the chromatic aberration effect."""
	
	dofAperture = None
	"""Path of the aperture shape texture file."""
	
	dofApertureRotation = None
	"""Rotation of the aperture shape texture."""
	
	dofEnabled = None
	"""Enables the depth of field effect."""
	
	dofFarBlur = None
	"""Far blur of the depth of field."""
	
	dofFocusDistance = None
	"""Focal distance of the depth of field."""
	
	dofFocusdofMaxBokehSizeDistance = None
	"""Maximum bokeh size of the depth of field."""
	
	dofNearBlur = None
	"""Near blur scale of the depth of field."""
	
	dofSwirlVignette = None
	"""Swirl vignette amount of the depth of field."""
	
	flareSize = None
	"""Size of the lens flare effect."""
	
	flareStrength = None
	"""Strength of the lens flare effect."""
	
	flareThreshold = None
	"""Threshold of the lens flare effect."""
	
	safeFrameEnabled = None
	"""Displays the safe frame in the viewport."""
	
	safeFrameOpacity = None
	"""Opacity of the safe frame display."""
	

class CameraObject.CameraLimits:
	"""
	Camera Limits Settings
	"""
	
	farLimit = None
	"""The far orbit limit distance."""
	
	farLimitEnabled = None
	"""Enables the far orbit distance limit."""
	
	nearLimit = None
	"""The near orbit limit distance."""
	
	nearLimitEnabled = None
	"""Enables the near orbit distance limit."""
	
	panLimit = None
	"""Limits the panning to either the Y-axis or completly (valid values are: 'Off', 'YAxis', 'Locked')."""
	
	pitchLimitEnabled = None
	"""Enables the pitch angle limit."""
	
	pitchLimitMax = None
	"""The maximum pitch angle, in degrees."""
	
	pitchLimitMin = None
	"""The minimum pitch angle, in degrees."""
	
	useLimitsInViewport = None
	"""Enables use of camera motion limits in the viewport."""
	
	yawLimitEnabled = None
	"""Enables the yaw angle limit."""
	
	yawLimitMax = None
	"""The maximum yaw limit angle, in degrees."""
	
	yawLimitMin = None
	"""The minimum yaw limit angle, in degrees."""
	
	yawLimitOffset = None
	"""The offset of the yaw limit angle, in degrees."""
	

class CameraObject.CameraPostEffect:
	"""
	Camera Post Effect
	"""
	
	bloomBrigtness = None
	"""Brightness multiplier for the bloom effect."""
	
	bloomSize = None
	"""Size scalar for the bloom effect."""
	
	contrast = None
	"""Contrast multiplier."""
	
	contrastCenter = None
	"""A value above which color values are brightened, and below which color values are darkened to achive the contrast effect."""
	
	exposure = None
	"""Exposure multiplier."""
	
	grainSharpness = None
	"""Sharpness scalar for the film grain effect."""
	
	grainStrength = None
	"""Strength multiplier for the film grain effect."""
	
	saturation = None
	"""Adjusts the intensity of color saturation (default is 1.0)."""
	
	sharpen = None
	"""Strength of the edge sharpening effect."""
	
	sharpenLimit = None
	"""A numerical limit on the stength of the edge sharpening effect."""
	
	toneMappingMode = None
	"""Tone mapping mode (allowed values are: 'Linear', 'Reinhard', 'Filmic')"""
	
	vignetteSoftness = None
	"""Softness scalar for the vignette effect."""
	
	vignetteStrength = None
	"""Strength multiplier for the vignette effect."""
	

class CompleteLightingBakerMap:
	"""
	Complete Lighting Baker Map Settings
	"""
	
	dither = None
	"""Determines whether this map output will be dithered."""
	
	enabled = None
	"""Whether or not this Baker Map should render when baking."""
	
	suffix = None
	"""The output suffix of the current Baker Map."""
	
	def resetSuffix():
		"""
		Resets the current map suffix to its default.
		"""
		pass

class CurvatureBakerMap:
	"""
	Curvature Baker Map Settings
	"""
	
	dither = None
	"""Determines whether this map output will be dithered."""
	
	enabled = None
	"""Whether or not this Baker Map should render when baking."""
	
	strength = None
	"""Determines the strength of the curvature output."""
	
	suffix = None
	"""The output suffix of the current Baker Map."""
	
	def resetSuffix():
		"""
		Resets the current map suffix to its default.
		"""
		pass

class ExternalObject:
	"""
	External Object
	"""
	
	collapsed = None
	"""Controls the display of the object's children in the outline view."""
	
	locked = None
	"""Controls the locking of object settings in the user interface."""
	
	name = None
	"""The name of the object."""
	
	parent = None
	"""The parent of the object."""
	
	path = None
	"""Path to a model file. If this path is altered, a new model will be loaded in place of the old one."""
	
	position = None
	"""The position of the object, as a list of 3 floats."""
	
	rotation = None
	"""The rotation of the object, as a list of 3 floats."""
	
	scale = None
	"""The scale of the object, as a list of 3 floats."""
	
	visible = None
	"""Controls object viewport visibility."""
	
	def destroy():
		"""
		Destroys the object and removes it from the scene.
		"""
		pass
	def duplicate(name=''):
		"""
		Duplicates the object, optionally assigning it a new name. Returns the new object.
		"""
		pass
	def findInChildren(searchStr):
		"""
		Finds and returns an object with a name matching 'searchStr', parented under this object. The search recursively checks all child objects.
		"""
		pass
	def getChildren():
		"""
		Returns a list of all immediate children of the object.
		"""
		pass
	def setKeyframe(lerp):
		"""
		Sets a keyframe on this object with the assigned interpolation function ("linear", "spline", or "splineBreak"). This setting defaults to editor's default.
		"""
		pass

class FogObject:
	"""
	Fog Object
	"""
	
	collapsed = None
	"""Controls the display of the object's children in the outline view."""
	
	color = None
	"""The color of the fog effect, as a list of 3 floats for RGB color."""
	
	dispersion = None
	"""A scalar specifying the dispersion, or light scatter, property of the fog effect."""
	
	distance = None
	"""The distance of the fog effect."""
	
	lightIllum = None
	"""A scalar specifying the degree to which lights affect the fog."""
	
	locked = None
	"""Controls the locking of object settings in the user interface."""
	
	name = None
	"""The name of the object."""
	
	opacity = None
	"""The maximum opacity of the fog effect."""
	
	parent = None
	"""The parent of the object."""
	
	skyIllum = None
	"""A scalar specifying the degree to which sky illumination affects the fog."""
	
	type = None
	"""The falloff type of the fog effect. Must be one of the following values: 'Linear' 'Distance Squared' 'Exponential'."""
	
	visible = None
	"""Controls object viewport visibility."""
	
	def destroy():
		"""
		Destroys the object and removes it from the scene.
		"""
		pass
	def duplicate(name=''):
		"""
		Duplicates the object, optionally assigning it a new name. Returns the new object.
		"""
		pass
	def findInChildren(searchStr):
		"""
		Finds and returns an object with a name matching 'searchStr', parented under this object. The search recursively checks all child objects.
		"""
		pass
	def getChildren():
		"""
		Returns a list of all immediate children of the object.
		"""
		pass
	def setKeyframe(lerp):
		"""
		Sets a keyframe on this object with the assigned interpolation function ("linear", "spline", or "splineBreak"). This setting defaults to editor's default.
		"""
		pass

class HeightBakerMap:
	"""
	Height Baker Map Settings
	"""
	
	dither = None
	"""Determines whether this map output will be dithered."""
	
	enabled = None
	"""Whether or not this Baker Map should render when baking."""
	
	innerDistance = None
	"""Inner height map distance from the low poly mesh, in world units. This value maps to black in the height map."""
	
	outerDistance = None
	"""Outer height map distance from the low poly mesh, in world units. This value maps to white in the height map."""
	
	suffix = None
	"""The output suffix of the current Baker Map."""
	
	def resetSuffix():
		"""
		Resets the current map suffix to its default.
		"""
		pass

class Image:
	"""
	A CPU-side image. Used for image loading and saving, and pixel manipulations. See mset.Texture for material and rendering uses.
	"""
	
	def compressBCn(mode):
		"""
		Encodes the image in a GPU-friendly block-compressed format. Currently supported modes are 4, 5, 6, and 7. Source images must be in an 8bit-per-channel color mode (such as BGRA8 or R8), except for mode 6, which requires a floating point color format.BC4 (mode=4) encodes grayscale in 4 bits per pixel.BC5 (mode=5) encodes two color channels in 8 bits per pixel. This is often useful for normal maps.BC6H(mode=6) encodes HDR RGB color in 8 bits per pixel. This is useful for high dynamic range images, such as backgrounds or panoramas.BC7 (mode=7) encodes RGB color and an alpha channel in 8 bits per pixel.
		"""
		pass
	def convertPixelFormat(format):
		"""
		Converts the image to the specified format. Some formats of interest:BGRA8: 0RGBA16: 1RGBA_FLOAT16: 2RGBA_FLOAT32: 3RGB10_A2: 5R8: 13R16: 14RG8: 15RG16: 16R_FLOAT16: 17RG_FLOAT16: 18R_FLOAT32: 19RG_FLOAT32: 20R11G11B10_FLOAT: 21
		"""
		pass
	def createTexture(sRGB=True):
		"""
		Creates a mset.Texture object from the image contents, ready for GPU use.
		"""
		pass
	def flipVertical():
		"""
		Vertically flips an image. Some pixel formats, such as BC7, may not be flippable.
		"""
		pass
	def generateMipmaps(sRGB=False):
		"""
		Generates mipmaps for the image. Can optionally account for sRGB color space.
		"""
		pass
	def getPixelFormat():
		"""
		Returns the current pixel format, or -1 if the image is invalid. See convertPixelFormat() for a list of format values.
		"""
		pass
	def writeOut(path):
		"""
		Writes the image contents to a file on disk. The file format is determined by the file extension.
		"""
		pass

class LightObject:
	"""
	Light Object
	"""
	
	brightness = None
	"""The brightness of the light."""
	
	castShadows = None
	"""Enables the casting of shadows by the light."""
	
	collapsed = None
	"""Controls the display of the object's children in the outline view."""
	
	color = None
	"""The color of the light."""
	
	gelPath = None
	"""Path of image to mask light shape."""
	
	gelTile = None
	"""Tiling scalar for the gel texture."""
	
	lengthX = None
	"""The length along the X axis of the light source."""
	
	lengthY = None
	"""The length along the Y axis of the light source."""
	
	lightType = None
	"""The type of the light (valid values are 'directional', 'spot', 'omni'"""
	
	locked = None
	"""Controls the locking of object settings in the user interface."""
	
	name = None
	"""The name of the object."""
	
	parent = None
	"""The parent of the object."""
	
	position = None
	"""The position of the object, as a list of 3 floats."""
	
	rotation = None
	"""The rotation of the object, as a list of 3 floats."""
	
	scale = None
	"""The scale of the object, as a list of 3 floats."""
	
	spotAngle = None
	"""The spot angle, in degrees, for use by spot lights only."""
	
	spotSharpness = None
	"""The sharpness of the spotlight shape, for use by spot lights only."""
	
	spotVignette = None
	"""The degree of spotlight vignette, for use by spot lights only."""
	
	visible = None
	"""Controls object viewport visibility."""
	
	visibleShape = None
	"""Makes the light source shape visible in final renders."""
	
	width = None
	"""The radius of the light source."""
	
	def destroy():
		"""
		Destroys the object and removes it from the scene.
		"""
		pass
	def duplicate(name=''):
		"""
		Duplicates the object, optionally assigning it a new name. Returns the new object.
		"""
		pass
	def findInChildren(searchStr):
		"""
		Finds and returns an object with a name matching 'searchStr', parented under this object. The search recursively checks all child objects.
		"""
		pass
	def getChildren():
		"""
		Returns a list of all immediate children of the object.
		"""
		pass
	def setKeyframe(lerp):
		"""
		Sets a keyframe on this object with the assigned interpolation function ("linear", "spline", or "splineBreak"). This setting defaults to editor's default.
		"""
		pass

class LightingBakerMap:
	"""
	Complete Lighting Baker Map Settings
	"""
	
	dither = None
	"""Determines whether this map output will be dithered."""
	
	enableSkybox = None
	"""Determines whether the skybox will be taken into account when rendering this map."""
	
	enabled = None
	"""Whether or not this Baker Map should render when baking."""
	
	ignoreGroups = None
	"""Determines whether bake groups will be ignored when rendering this map. Useful for casting shadows across bake groups."""
	
	suffix = None
	"""The output suffix of the current Baker Map."""
	
	def resetSuffix():
		"""
		Resets the current map suffix to its default.
		"""
		pass

class Material:
	"""
	Material
	"""
	
	albedo = None
	"""The MaterialSubroutine currently assigned to the Albedo Slot"""
	
	clearCoatMicrosurface = None
	"""The MaterialSubroutine currently assigned to the Clear Coat Microsurface Slot"""
	
	clearCoatReflection = None
	"""The MaterialSubroutine currently assigned to the Clear Coat Reflection Slot"""
	
	clearcoatReflectivity = None
	"""The MaterialSubroutine currently assigned to the Clear Coat Reflectivity Slot"""
	
	diffusion = None
	"""The MaterialSubroutine currently assigned to the Diffusion Slot"""
	
	displacement = None
	"""The MaterialSubroutine currently assigned to the Displacement Slot"""
	
	emission = None
	"""The MaterialSubroutine currently assigned to the Emission Slot"""
	
	extra = None
	"""The MaterialSubroutine currently assigned to the Extra Slot"""
	
	microsurface = None
	"""The MaterialSubroutine currently assigned to the Microsurface Slot"""
	
	name = None
	"""The name of the Material. Please note that Materials must have unique names in Toolbag scenes."""
	
	occlusion = None
	"""The MaterialSubroutine currently assigned to the Occlusion Slot"""
	
	reflection = None
	"""The MaterialSubroutine currently assigned to the Reflection Slot"""
	
	reflectivity = None
	"""The MaterialSubroutine currently assigned to the Reflectivity Slot"""
	
	surface = None
	"""The MaterialSubroutine currently assigned to the Surface Slot"""
	
	texture = None
	"""The MaterialSubroutine used for texture parameters"""
	
	transmission = None
	"""The MaterialSubroutine currently assigned to the Transmission Slot"""
	
	transparency = None
	"""The MaterialSubroutine currently assigned to the Transparency Slot"""
	
	def assign(object, includeChildren=True):
		"""
		Assigns the material to a scene object. If 'includeChildren' is true, this material will also be applied to the children of the object.
		"""
		pass
	def destroy():
		"""
		Destroys the Material and removes it from the scene.
		"""
		pass
	def duplicate(name=''):
		"""
		Duplicates the Material, optionally assigning it a name. If no name is specified, one will be automatically generated.Returns the new material.
		"""
		pass
	def exportFile(path):
		"""
		Exports this material to the path specified.
		"""
		pass
	def getAssignedObjects():
		"""
		Returns a list of all scene objects to which this material is assigned.
		"""
		pass
	def getCustomShader():
		"""
		Returns the name of the custom shader file, or an empty string if there is none.
		"""
		pass
	def getGroup():
		"""
		Returns the string name of the group the material is assigned to or an empty string, if the material is in no group.
		"""
		pass
	def getSubroutine(subroutine):
		"""
		Returns the subroutine in a given slot, specified by string name. See also setSubroutine().
		"""
		pass
	def renderPreview(width, height):
		"""
		Renders the material, applied to a sample mesh, to a preview image. Returns an mset.Image instance.
		"""
		pass
	def setCustomShader(shaderFile):
		"""
		Assigns a custom shader to the material. The supplied file name must refer to a .frag or .vert file in data/shader/mat/custom. Passing an empty string will unset any custom shader present.
		"""
		pass
	def setGroup(name):
		"""
		Assigns the material to a new or existing group. Use '' to assign the material to no group.
		"""
		pass
	def setKeyframe(lerp):
		"""
		Sets a keyframe on this object with the assigned interpolation function ("linear", "spline", or "splineBreak"). This setting defaults to editor's default.
		"""
		pass
	def setSubroutine(subroutine, shader):
		"""
		Assigns a shader type to a given subroutine. Both parameters are string names. 'shader' must be a valid shader name, and 'subroutine' must be one of: 'subdivision', 'displacement', 'surface', 'microsurface', 'albedo', 'diffusion', 'reflectivity', 'reflection', 'secondaryReflection', 'occlusion', 'emissive', 'transparency', 'extra', 'texture'.
		"""
		pass

class MaterialSubroutine:
	"""
	Material Subroutine
	"""
	
	def getField(name):
		"""
		Returns the value of a field.
		"""
		pass
	def getFieldNames():
		"""
		Returns a list of all field names of the subroutine.
		"""
		pass
	def setField(name, value):
		"""
		Sets the value of a field. Texture fields may be set by either passing a string path or an mset.Texture instance.
		"""
		pass

class Mesh:
	"""
	Mesh
	"""
	
	bitangents = None
	"""Mesh bitangents, as a list of float groups of 3 ( e.g. [x,y,z, x,y,z] )"""
	
	colors = None
	"""Mesh colors, as a list of float groups of 4 ( e.g. [r,g,b,a, r,g,b,a] )"""
	
	normals = None
	"""Mesh normals, as a list of float groups of 3 ( e.g. [x,y,z, x,y,z] )"""
	
	polygons = None
	"""Mesh polygon groups, as a list of int groups of 2, start and count ( e.g. [0,2, 1,2] )"""
	
	secondaryUVs = None
	"""Mesh secondary texture coordinates, as a list of float groups of 2 ( e.g. [u,v, u,v] )"""
	
	tangents = None
	"""Mesh tangents, as a list of float groups of 3 ( e.g. [x,y,z, x,y,z] )"""
	
	triangles = None
	"""Mesh triangle indices, as a list of int groups of 3 ( e.g. [0,1,2, 1,3,2] )"""
	
	uvs = None
	"""Mesh texture coordinates as a list of float groups of 2 ( e.g. [u,v, u,v] )"""
	
	vertices = None
	"""Mesh vertex positions, as a list of float groups of 3 ( e.g. [x,y,z, x,y,z] )"""
	

class MeshObject:
	"""
	Mesh Object
	"""
	
	castShadows = None
	"""Enables casting of shadows from the mesh."""
	
	collapsed = None
	"""Controls the display of the object's children in the outline view."""
	
	cullBackFaces = None
	"""Enables the culling of back faces during render."""
	
	fixMirroredTangents = None
	"""Fix tangent issues that arise with mirrored UVs in certain tangent spaces."""
	
	locked = None
	"""Controls the locking of object settings in the user interface."""
	
	mesh = None
	"""The mesh containing vertex data."""
	
	name = None
	"""The name of the object."""
	
	parent = None
	"""The parent of the object."""
	
	position = None
	"""The position of the object, as a list of 3 floats."""
	
	rotation = None
	"""The rotation of the object, as a list of 3 floats."""
	
	scale = None
	"""The scale of the object, as a list of 3 floats."""
	
	tangentSpace = None
	"""Mesh tangent space for normal mapping. This must be one of the following values: 'Custom' 'Marmoset', 'Mikk', 'Maya', '3D Studio Max', 'Unity'"""
	
	visible = None
	"""Controls object viewport visibility."""
	
	def addSubmesh(name, material=None, startIndex=0, indexCount=-1):
		"""
		Adds and returns a SubMeshObject to the MeshObject, rendering the specified range of indices.name: Name of the SubMeshObjectmaterial: The Material assigned to the submesh.startIndex: The index of the first vertex of the submesh.indexCount: The number of indices following 'startIndex', or -1 to cover all remaining indices in the mesh.
		"""
		pass
	def destroy():
		"""
		Destroys the object and removes it from the scene.
		"""
		pass
	def duplicate(name=''):
		"""
		Duplicates the object, optionally assigning it a new name. Returns the new object.
		"""
		pass
	def findInChildren(searchStr):
		"""
		Finds and returns an object with a name matching 'searchStr', parented under this object. The search recursively checks all child objects.
		"""
		pass
	def getChildren():
		"""
		Returns a list of all immediate children of the object.
		"""
		pass
	def setKeyframe(lerp):
		"""
		Sets a keyframe on this object with the assigned interpolation function ("linear", "spline", or "splineBreak"). This setting defaults to editor's default.
		"""
		pass

class MetalnessBakerMap:
	"""
	Metalness Baker Map Settings
	"""
	
	enabled = None
	"""Whether or not this Baker Map should render when baking."""
	
	metalnessThreshold = None
	"""Any specular value above this threshold will be considered metal."""
	
	suffix = None
	"""The output suffix of the current Baker Map."""
	
	def resetSuffix():
		"""
		Resets the current map suffix to its default.
		"""
		pass

class NormalBakerMap:
	"""
	Normal Baker Map Settings
	"""
	
	dither = None
	"""Determines whether this map output will be dithered."""
	
	enabled = None
	"""Whether or not this Baker Map should render when baking."""
	
	flipX = None
	"""Determines whether the normal map's X channel will be flipped."""
	
	flipY = None
	"""Determines whether the normal map's Y channel will be flipped."""
	
	flipZ = None
	"""Determines whether the normal map's Z channel will be flipped."""
	
	suffix = None
	"""The output suffix of the current Baker Map."""
	
	def resetSuffix():
		"""
		Resets the current map suffix to its default.
		"""
		pass

class PositionBakerMap:
	"""
	Position Baker Map Settings
	"""
	
	enabled = None
	"""Whether or not this Baker Map should render when baking."""
	
	normalization = None
	"""The method by which you normalize position data."""
	
	suffix = None
	"""The output suffix of the current Baker Map."""
	
	def resetSuffix():
		"""
		Resets the current map suffix to its default.
		"""
		pass

class PyTurntableObject:
	"""
	Turntable Object
	"""
	
	collapsed = None
	"""Controls the display of the object's children in the outline view."""
	
	enabled = None
	"""Enables the active motion of the turntable object."""
	
	locked = None
	"""Controls the locking of object settings in the user interface."""
	
	name = None
	"""The name of the object."""
	
	parent = None
	"""The parent of the object."""
	
	position = None
	"""The position of the object, as a list of 3 floats."""
	
	rotation = None
	"""The rotation of the object, as a list of 3 floats."""
	
	scale = None
	"""The scale of the object, as a list of 3 floats."""
	
	spinRate = None
	"""The rate at which the turntable object rotates, in degrees per second."""
	
	visible = None
	"""Controls object viewport visibility."""
	
	def destroy():
		"""
		Destroys the object and removes it from the scene.
		"""
		pass
	def duplicate(name=''):
		"""
		Duplicates the object, optionally assigning it a new name. Returns the new object.
		"""
		pass
	def findInChildren(searchStr):
		"""
		Finds and returns an object with a name matching 'searchStr', parented under this object. The search recursively checks all child objects.
		"""
		pass
	def getChildren():
		"""
		Returns a list of all immediate children of the object.
		"""
		pass
	def setKeyframe(lerp):
		"""
		Sets a keyframe on this object with the assigned interpolation function ("linear", "spline", or "splineBreak"). This setting defaults to editor's default.
		"""
		pass

class RenderObject:
	"""
	Render Object
	"""
	
	collapsed = None
	"""Controls the display of the object's children in the outline view."""
	
	locked = None
	"""Controls the locking of object settings in the user interface."""
	
	name = None
	"""The name of the object."""
	
	parent = None
	"""The parent of the object."""
	
	visible = None
	"""Controls object viewport visibility."""
	
	def destroy():
		"""
		Destroys the object and removes it from the scene.
		"""
		pass
	def duplicate(name=''):
		"""
		Duplicates the object, optionally assigning it a new name. Returns the new object.
		"""
		pass
	def findInChildren(searchStr):
		"""
		Finds and returns an object with a name matching 'searchStr', parented under this object. The search recursively checks all child objects.
		"""
		pass
	def getChildren():
		"""
		Returns a list of all immediate children of the object.
		"""
		pass
	def getRenderOptions():
		"""
		Returns a copy of the current scene render options. See RenderOptions.
		"""
		pass
	def setKeyframe(lerp):
		"""
		Sets a keyframe on this object with the assigned interpolation function ("linear", "spline", or "splineBreak"). This setting defaults to editor's default.
		"""
		pass
	def setRenderOptions(options):
		"""
		Sets the current scene render options. 'options' must be an instance of RenderOptions.
		"""
		pass

class RenderOptions:
	"""
	Scene Render Options
	"""
	
	drawWireframe = None
	"""Enables the rendering of mesh wireframes."""
	
	shadowCascadeDistance = None
	"""A bias value for how distance the furthest shadow cascade is from the camera."""
	
	shadowQuality = None
	"""Shadow quality. Valid values are 'Low', 'High', and 'Mega'."""
	
	useShadowCascades = None
	"""Use cascaded shadow maps for directional lights. This can provide better resolution distribution over larger scenes."""
	
	wireframeColor = None
	"""Wireframe color as an RGBA array."""
	

class SceneObject:
	"""
	Scene Object
	"""
	
	collapsed = None
	"""Controls the display of the object's children in the outline view."""
	
	locked = None
	"""Controls the locking of object settings in the user interface."""
	
	name = None
	"""The name of the object."""
	
	parent = None
	"""The parent of the object."""
	
	visible = None
	"""Controls object viewport visibility."""
	
	def destroy():
		"""
		Destroys the object and removes it from the scene.
		"""
		pass
	def duplicate(name=''):
		"""
		Duplicates the object, optionally assigning it a new name. Returns the new object.
		"""
		pass
	def findInChildren(searchStr):
		"""
		Finds and returns an object with a name matching 'searchStr', parented under this object. The search recursively checks all child objects.
		"""
		pass
	def getChildren():
		"""
		Returns a list of all immediate children of the object.
		"""
		pass
	def setKeyframe(lerp):
		"""
		Sets a keyframe on this object with the assigned interpolation function ("linear", "spline", or "splineBreak"). This setting defaults to editor's default.
		"""
		pass

class ShadowCatcherObject:
	"""
	Shadow Catcher Object
	"""
	
	collapsed = None
	"""Controls the display of the object's children in the outline view."""
	
	edgeFade = None
	"""Enables a fading of shadow opacity towards the edges of the shadow catcher plane."""
	
	fadeTexturePath = None
	"""File path of the fade texture, which is used to control the shadow fade pattern."""
	
	locked = None
	"""Controls the locking of object settings in the user interface."""
	
	name = None
	"""The name of the object."""
	
	opacity = None
	"""The opacity of the shadow catcher."""
	
	parent = None
	"""The parent of the object."""
	
	position = None
	"""The position of the object, as a list of 3 floats."""
	
	rotation = None
	"""The rotation of the object, as a list of 3 floats."""
	
	scale = None
	"""The scale of the object, as a list of 3 floats."""
	
	skyShadow = None
	"""Enables receiving shadow from the sky light (ray tracing only)."""
	
	textureChannel = None
	"""The active channel in the fade texture (must be one of: 'R', 'G', 'B', 'A')."""
	
	visible = None
	"""Controls object viewport visibility."""
	
	def destroy():
		"""
		Destroys the object and removes it from the scene.
		"""
		pass
	def duplicate(name=''):
		"""
		Duplicates the object, optionally assigning it a new name. Returns the new object.
		"""
		pass
	def findInChildren(searchStr):
		"""
		Finds and returns an object with a name matching 'searchStr', parented under this object. The search recursively checks all child objects.
		"""
		pass
	def getChildren():
		"""
		Returns a list of all immediate children of the object.
		"""
		pass
	def setKeyframe(lerp):
		"""
		Sets a keyframe on this object with the assigned interpolation function ("linear", "spline", or "splineBreak"). This setting defaults to editor's default.
		"""
		pass

class SkyBoxObject:
	"""
	Skybox Scene Object
	"""
	
	brightness = None
	"""The brightness of the skybox."""
	
	collapsed = None
	"""Controls the display of the object's children in the outline view."""
	
	locked = None
	"""Controls the locking of object settings in the user interface."""
	
	name = None
	"""The name of the object."""
	
	parent = None
	"""The parent of the object."""
	
	rotation = None
	"""The current rotation angle of the skybox."""
	
	visible = None
	"""Controls object viewport visibility."""
	
	def clearLightChildren():
		"""
		Clears all light children of this skybox.
		"""
		pass
	def destroy():
		"""
		Destroys the object and removes it from the scene.
		"""
		pass
	def duplicate(name=''):
		"""
		Duplicates the object, optionally assigning it a new name. Returns the new object.
		"""
		pass
	def findInChildren(searchStr):
		"""
		Finds and returns an object with a name matching 'searchStr', parented under this object. The search recursively checks all child objects.
		"""
		pass
	def getChildren():
		"""
		Returns a list of all immediate children of the object.
		"""
		pass
	def importImage(path):
		"""
		Imports an image to use for this skybox.
		"""
		pass
	def loadSky(path):
		"""
		Loads a .tbsky file in place of the current sky.
		"""
		pass
	def renderPreview(width, height):
		"""
		Renders the sky background, in latitude-longitude format, to a preview image. Returns an mset.Image instance.
		"""
		pass
	def saveSky(path):
		"""
		Saves the current sky to the specified file path as a .tbsky archive.
		"""
		pass
	def setKeyframe(lerp):
		"""
		Sets a keyframe on this object with the assigned interpolation function ("linear", "spline", or "splineBreak"). This setting defaults to editor's default.
		"""
		pass

class SubMeshObject:
	"""
	Sub Mesh Object
	"""
	
	collapsed = None
	"""Controls the display of the object's children in the outline view."""
	
	indexCount = None
	"""The index count of the submesh."""
	
	locked = None
	"""Controls the locking of object settings in the user interface."""
	
	material = None
	"""The material assigned to the submesh."""
	
	name = None
	"""The name of the object."""
	
	parent = None
	"""The parent of the object."""
	
	startIndex = None
	"""The first index of the submesh."""
	
	visible = None
	"""Controls object viewport visibility."""
	
	def destroy():
		"""
		Destroys the object and removes it from the scene.
		"""
		pass
	def duplicate(name=''):
		"""
		Duplicates the object, optionally assigning it a new name. Returns the new object.
		"""
		pass
	def findInChildren(searchStr):
		"""
		Finds and returns an object with a name matching 'searchStr', parented under this object. The search recursively checks all child objects.
		"""
		pass
	def getChildren():
		"""
		Returns a list of all immediate children of the object.
		"""
		pass
	def setKeyframe(lerp):
		"""
		Sets a keyframe on this object with the assigned interpolation function ("linear", "spline", or "splineBreak"). This setting defaults to editor's default.
		"""
		pass

class Texture:
	"""
	GPU Texture
	"""
	
	anisotropicFiltering = None
	"""Sets the degree of anisotropic filtering applied to this texture."""
	
	path = None
	"""The file path of the texture. Note: You cannot set the path of a mset.Texture, only get it."""
	
	sRGB = None
	"""Determines whether the texture is sampled in sRGB color space."""
	
	useFiltering = None
	"""Determines whether the texture is filtered bilinearly (smooth) or by nearest neighbor (pixelated)."""
	
	useMipmaps = None
	"""Determines whether mipmaps are used on the texture."""
	
	wrapping = None
	"""Sets the type of texture wrapping applied to this texture. """
	
	def renderPreview(width, height):
		"""
		Renders a preview of the texture, at the given resolution. Returns an mset.Image instance.
		"""
		pass

class ThicknessBakerMap:
	"""
	Thickness Baker Map Settings
	"""
	
	dither = None
	"""Determines whether this map output will be dithered."""
	
	enabled = None
	"""Whether or not this Baker Map should render when baking."""
	
	rayCount = None
	"""The number of rays used for thickness baking."""
	
	suffix = None
	"""The output suffix of the current Baker Map."""
	
	def resetSuffix():
		"""
		Resets the current map suffix to its default.
		"""
		pass

class Timeline:
	"""
	Animation Timeline
	"""
	
	currentFrame = None
	"""Current animation frame. This value must be within the valid range of 0 to totalFrames."""
	
	playbackSpeed = None
	"""The current playback speed. This value controls the apparent speed of playback in the viewport, but does not affect exported animation length."""
	
	selectionEnd = None
	"""The last frame of the selected time range. Must be less than totalFrames and greater than zero."""
	
	selectionStart = None
	"""The first frame of the selected time range. Must be less than totalFrames and greater than zero."""
	
	totalFrames = None
	"""Total frame count for the animation. This value must be greater than zero."""
	
	def getFrameRate():
		"""
		Returns the scene's animation frame rate, in frames per second.
		"""
		pass
	def getTime():
		"""
		Returns the current animation time, in seconds.
		"""
		pass
	def pause():
		"""
		Stops animation playback.
		"""
		pass
	def play():
		"""
		Activates animation playback.
		"""
		pass
	def resample(frameRate):
		"""
		Alters the animation timeline's frame rate, in frames per second. This will resample existing keyframes to fit the new frame rate, and alter the appropriate frame counts.
		"""
		pass
	def setTime(time):
		"""
		Sets the current animation time, in seconds. This time may be rounded to the nearest frame.
		"""
		pass

class TransformObject:
	"""
	Transform Object
	"""
	
	collapsed = None
	"""Controls the display of the object's children in the outline view."""
	
	locked = None
	"""Controls the locking of object settings in the user interface."""
	
	name = None
	"""The name of the object."""
	
	parent = None
	"""The parent of the object."""
	
	position = None
	"""The position of the object, as a list of 3 floats."""
	
	rotation = None
	"""The rotation of the object, as a list of 3 floats."""
	
	scale = None
	"""The scale of the object, as a list of 3 floats."""
	
	visible = None
	"""Controls object viewport visibility."""
	
	def destroy():
		"""
		Destroys the object and removes it from the scene.
		"""
		pass
	def duplicate(name=''):
		"""
		Duplicates the object, optionally assigning it a new name. Returns the new object.
		"""
