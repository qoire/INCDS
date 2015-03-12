class phaseModule():
    # Alex keep your code here
    def __init__(self):
        # initiate self variables here
		self.phase_list = []
		self.current_phase = 0
		self.counter = 0
		self.increment=30*3.1415/180
		self.prev_phase=None
		self.prev_mag=None
		self.is_phase_going_negative=None
		

    def setPhase(self, phase):
        self.current_phase = phase

    def phaseChange(self, cur_mag):
		if self.counter==0:
			next_phase=5*3.1415/180
			self.ini_mag=cur_mag
			self.counter=self.counter+1
		elif self.counter==1:
			if cur_mag > self.ini_mag:
				next_phase=-10*3.1415/180
				self.prev_phase=0
				self.prev_mag=cur_mag
				self.is_phase_going_negative=True
				self.counter=self.counter+1
			else:
				next_phase=10*3.1415/180
				self.prev_phase=0
				self.prev_mag=cur_mag
				self.is_phase_going_negative=False
				self.counter=self.counter+1
		else:
			if cur_mag <= self.prev_mag:
				if self.is_phase_going_negative==True:
					next_phase=self.prev_phase-self.increment
					self.prev_mag=cur_mag
				else:
					next_phase=self.prev_phase+self.increment
					self.prev_mag=cur_mag
				self.prev_phase=next_phase
			else:
				self.increment=self.increment/2
				self.prev_mag=cur_mag
				if self.is_phase_going_negative==True:
					next_phase=self.prev_phase+self.increment
				else:
					next_phase=self.prev_phase-self.increment
				self.is_phase_going_negative=not(self.is_phase_going_negative)
				self.prev_phase=next_phase
				
        #main function that will contain the phase change algorithm
		print " self.increment=%s " %self.increment
		return next_phase