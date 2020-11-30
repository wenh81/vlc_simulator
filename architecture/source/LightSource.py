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
        self.intensity = {"time": [], "intensity": []}

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

    def convertToOpticalPower(self, current):
        """Converts a given current value into an output optical power."""
        pass
    

    def getIntensityAtDistance(self, distance):
        """Returns the intensity (W) for a given distance (m)."""
        pass
    

    def loadsJSONData(self):
        """Loads in the JSON data for that light source."""
        pass
    

    def getLightType(self):
        """Returns value of self.light_type"""
        
        return self.light_type

    def setLightType(self, light_type):
        """Set new value for self.light_type"""
        
        self.light_type = light_type

    def getPsd(self):
        """Returns value of self.psd"""
        
        return self.psd

    def setPsd(self, psd):
        """Set new value for self.psd"""
        
        self.psd = psd

    def getIntensity(self):
        """Returns value of self.intensity"""
        
        return self.intensity

    def setIntensity(self, intensity):
        """Set new value for self.intensity"""
        
        self.intensity = intensity

    def getDatabase(self):
        """Returns value of self.database"""
        
        return self.database

    def setDatabase(self, database):
        """Set new value for self.database"""
        
        self.database = database

    def getPosition(self):
        """Returns value of self.position"""
        
        return self.position

    def setPosition(self, position):
        """Set new value for self.position"""
        
        self.position = position

    def getAngle(self):
        """Returns value of self.angle"""
        
        return self.angle

    def setAngle(self, angle):
        """Set new value for self.angle"""
        
        self.angle = angle

    def getLinearityCurve(self):
        """Returns value of self.linearity_curve"""
        
        return self.linearity_curve

    def setLinearityCurve(self, linearity_curve):
        """Set new value for self.linearity_curve"""
        
        self.linearity_curve = linearity_curve

    def getFOV(self):
        """Returns value of self.FOV"""
        
        return self.FOV

    def setFOV(self, FOV):
        """Set new value for self.FOV"""
        
        self.FOV = FOV
