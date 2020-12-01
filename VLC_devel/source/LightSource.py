from generalLibrary import timer_dec, sync_track

class LightSource(object):
    
    def __init__(self, light_type, position, angle, sync_obj):
        """Constructor of LightSource. Receives the light_type"""
        
        # Create sync object, and set debug and simulation path
        self.sync_obj = sync_obj
        
        self.DEBUG = self.sync_obj.getDebug("LightSource") or self.sync_obj.getDebug("all")
        
        self.sync_obj.appendToSimulationPath("LightSource")
        
        if self.DEBUG:
            print('Running LightSource...')
        
        # Stores the light type. Ex: LED, Laser, etc.
        self.light_type = "LED"

        # Stores the PSD (W/nm) over the wave number (nm)
        self.psd = {"wave_number": [], "psd": []}

        # Stores the intensities (W/m2) emitted by that light source over time (s).
        # self.intensity = {"time": [], "power": []}
        # Stores the power (W) emitted by that light source over time (s).
        self.power = {"time": [], "power": []}

        # Stores the path to the database file, from where we get all data for that light source.
        self.database = r"..\Databases"

        # Contains the position for that light source. Used for ray tracing, if appliable.
        self.position = position

        # Contains the angle for that light source. Used for ray tracing, if appliable.
        self.angle = angle

        # Curve that translates how to convert from drive current to optical power.
        self.linearity_curve = {"current": [], "optical_power": []}

        # Info regarding the FOV of such light source.
        self.FOV = None
        
        pass

    @sync_track
    def convertToOpticalPower(self, current):
        """Converts a given current value into an output optical power."""
        pass
    

    @sync_track
    def getIntensityAtDistance(self, distance):
        """Returns the intensity (W) for a given distance (m)."""
        pass
    

    @sync_track
    def loadsJSONData(self):
        """Loads in the JSON data for that light source."""
        pass
    

    @sync_track
    def getLightType(self):
        """Returns value of self.light_type"""
        
        return self.light_type

    @sync_track
    def setLightType(self, light_type):
        """Set new value for self.light_type"""
        
        self.light_type = light_type

    @sync_track
    def getPsd(self):
        """Returns value of self.psd"""
        
        return self.psd

    @sync_track
    def setPsd(self, psd):
        """Set new value for self.psd"""
        
        self.psd = psd

    @sync_track
    def getIntensity(self):
        """Returns value of self.intensity"""
        
        return self.intensity

    @sync_track
    def setIntensity(self, intensity):
        """Set new value for self.intensity"""
        
        self.intensity = intensity

    @sync_track
    def getDatabase(self):
        """Returns value of self.database"""
        
        return self.database

    @sync_track
    def setDatabase(self, database):
        """Set new value for self.database"""
        
        self.database = database

    @sync_track
    def getPosition(self):
        """Returns value of self.position"""
        
        return self.position

    @sync_track
    def setPosition(self, position):
        """Set new value for self.position"""
        
        self.position = position

    @sync_track
    def getAngle(self):
        """Returns value of self.angle"""
        
        return self.angle

    @sync_track
    def setAngle(self, angle):
        """Set new value for self.angle"""
        
        self.angle = angle

    @sync_track
    def getLinearityCurve(self):
        """Returns value of self.linearity_curve"""
        
        return self.linearity_curve

    @sync_track
    def setLinearityCurve(self, linearity_curve):
        """Set new value for self.linearity_curve"""
        
        self.linearity_curve = linearity_curve

    @sync_track
    def getFOV(self):
        """Returns value of self.FOV"""
        
        return self.FOV

    @sync_track
    def setFOV(self, FOV):
        """Set new value for self.FOV"""
        
        self.FOV = FOV

    def getSyncObj(self):
        """Returns value of self.sync_obj"""
        
        return self.sync_obj
    
    def setSyncObj(self, sync_obj):
        """Set new value for self.sync_obj"""
        
        self.sync_obj = sync_obj