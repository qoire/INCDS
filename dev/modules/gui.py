import wx   
  
class SliderFrame(wx.Frame):  
    def __init__(self):  
	  wx.Frame.__init__(self, None, -1, 'User Interface',size=(600, 300))  
	  panel = wx.Panel(self, -1)  
	  self.phase = 0
	  self.magnitude = 0
	  self.slider = wx.Slider(panel, -1, 0, -180, 180, pos=(40, 10),  size=(500, -1),style=wx.SL_HORIZONTAL | wx.SL_AUTOTICKS | wx.SL_LABELS,name="Phase")  
	  self.slider.SetTickFreq(5, 1)  
	  button=wx.Button(panel,-1,label="send",pos=(500,100), size=(50,20))
	  self.Bind(wx.EVT_BUTTON,self.printting,button)
	  wx.StaticText(panel,-1,"Phase",pos=(0,15))
	  wx.StaticText(panel,-1,"Magnitude \n in dB",pos=(0,100))
	  wx.StaticText(panel,-1,"Current Phase:",pos=(0,200))
	  wx.StaticText(panel,-1,"Current Magnitude:",pos=(0,220))
	  self.sc=wx.SpinCtrl(panel,-1,"",pos=(80,100),size=(100,30),style=wx.SP_ARROW_KEYS,min=0,max=60,initial=0)
	  self.label1=wx.StaticText (panel,-1,str(self.phase),pos=(140,200))
	  self.label2=wx.StaticText(panel,-1,str(self.magnitude),pos=(140,220))
    def printting (self,event):
	  print(self.sc.GetValue())
	  print(self.slider.GetValue())
	  self.label1.SetLabel(str(self.slider.GetValue()))
	  self.label2.SetLabel(str(self.sc.GetValue()))
	  

          
if __name__ == '__main__':  
    app = wx.PySimpleApp()  
    frame = SliderFrame()  
    frame.Show()  
    app.MainLoop()   
