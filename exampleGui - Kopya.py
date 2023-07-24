import ui
import chr
import dbg
import app
import background
import GLPythonNetworkStream
import GLPythonPlayer
import GLList
import GLPlayer
import GLConnect
import GLHelper
import math


class ExampleGui(ui.BoardWithTitleBar):
    def __init__(self):
        ui.BoardWithTitleBar.__init__(self)
        self.AddFlag("movable")
        self.AddFlag("float")
        self.SetPosition(200, 150)
        self.SetSize(360, 330)
        self.SetTitleName("GLBot++ Py Loader Example Gui")
        self.UI = UI()
        self.playerList = []

        self.CharacterInfoNameLabel = self.UI.Label(self, 20, 30, "CharacterInfoNameLabel")
        self.CharacterInfoLevelLabel = self.UI.Label(self, 20, 50, "CharacterInfoLevelLabel")
        self.CharacterInfoHPLabel = self.UI.Label(self, 20, 70, "CharacterInfoHPLabel")
        self.CharacterInfoSPLabel = self.UI.Label(self, 20, 90, "CharacterInfoSPLabel")
        self.CharacterInfoEXPLabel = self.UI.Label(self, 20, 110, "CharacterInfoEXPLabel")
        self.CharacterInfoYangLabel = self.UI.Label(self, 20, 130, "CharacterInfoYangLabel")
        self.PlayerListLabel = self.UI.Label(self, 140, 30, "PlayerListLabel")
        self.CHChangeInfoLabel = self.UI.Label(self, 20, 230, "CH Changer")
        self.MapChangeInfoLabel = self.UI.Label(self, 20, 280, "Map Changer")

        self.PlayerListBox = self.UI.ListBoxEx(self, 140, 50, 200, 100)

        self.DamageButton = self.UI.Button(self, 'Start Damage', '', 160, 165, self.DamageFunc , "large")
        self.DamageRangeLabel = self.UI.Label(self, 20, 167, "Range : ")
        self.DamageRangeEdit = self.UI.EditLine(self, "60", 60, 165, 20, 15, 20)
        self.DamageLimitLabel = self.UI.Label(self, 90, 167, "Limit : ")
        self.DamageLimitEdit = self.UI.EditLine(self, '10', 125, 165, 20, 15, 20)

        self.PickupButton = self.UI.Button(self, 'Start Pickup', '', 250, 165, self.PickupFunc , "large")

        self.WallHackButton = self.UI.ToggleButton(self, 'Wall Hack', '', 160, 200,
                                                (lambda arg='off': self.WallHackFunc(arg)),
                                                (lambda arg='on': self.WallHackFunc(arg)), "middle")

        self.MoveSpeedButton = self.UI.ToggleButton(self, 'Move Speed', '', 90, 200,
                                                (lambda arg='off': self.MoveSpeedFunc(arg)),
                                                (lambda arg='on': self.MoveSpeedFunc(arg)), "middle")

        self.MoveSpeedLabel = self.UI.Label(self, 20, 200, "Speed : ")
        self.MoveSpeedEdit = self.UI.EditLine(self, '40', 60, 200, 20, 15, 20)

        self.LevelBotButton = self.UI.ToggleButton(self, 'Level Bot', '', 250, 200,
                                                (lambda arg='off': self.LevelBotFunc(arg)),
                                                (lambda arg='on': self.LevelBotFunc(arg)), "large")

        self.CHChange1Button = self.UI.Button(self, '1', '', 20, 250, lambda: self.CHChangeFunc(1), "small")
        self.CHChange2Button = self.UI.Button(self, '2', '', 65, 250, lambda: self.CHChangeFunc(2), "small")
        self.CHChange3Button = self.UI.Button(self, '3', '', 110, 250, lambda: self.CHChangeFunc(3), "small")
        self.CHChange4Button = self.UI.Button(self, '4', '', 155, 250, lambda: self.CHChangeFunc(4), "small")
        self.CHChange5Button = self.UI.Button(self, '5', '', 200, 250, lambda: self.CHChangeFunc(5), "small")
        self.CHChange6Button = self.UI.Button(self, '6', '', 245, 250, lambda: self.CHChangeFunc(6), "small")

        self.MapChange1Button = self.UI.Button(self, 'Town1', '', 20, 300, lambda: self.MapChangeFunc("Town1"), "small")
        self.MapChange2Button = self.UI.Button(self, 'Town2', '', 65, 300, lambda: self.MapChangeFunc("Town2"), "small")
        self.MapChange3Button = self.UI.Button(self, 'Vadi', '', 110, 300, lambda: self.MapChangeFunc("map_a2"), "small")
        self.MapChange4Button = self.UI.Button(self, 'Desert', '', 155, 300, lambda: self.MapChangeFunc("metin2_map_n_desert_01"), "small")
        self.MapChange5Button = self.UI.Button(self, 'Sohan', '', 200, 300, lambda: self.MapChangeFunc("map_n_snowm_01"), "small")
        self.MapChange6Button = self.UI.Button(self, 'Doyum', '', 245, 300, lambda: self.MapChangeFunc("metin2_map_n_flame_01"), "small")


        self.PlayerListTick = 0
        self.LevelBotTick = 0
        self.DamageTick = 0
        self.GeneralTick = 0
        self.PickupTick = 0

        self.LevelBotStatus = False
        self.DamageStatus = False
        self.PickupStatus = False
        self.MoveSpeedStatus = False
        self.WallHackStatus = False
        self.MoveSpeedStateCount = 0
        self.LevelBotBeginPosition = GLPlayer.GetPixelPosition()

        self.Show()

    def OnUpdate(self):
        if GLPlayer.IsReady() and GLPlayer.IsOnline():
            if GLHelper.GetTime() - self.PlayerListTick >= 1000:
                self.UpdatePlayerList()
                self.UpdatePlayerInfo()
                self.PlayerListTick = GLHelper.GetTime()
            if GLHelper.GetTime() - self.LevelBotTick >= 100:
                self.AttackCloseMob()
                self.LevelBotTick = GLHelper.GetTime()
            if GLHelper.GetTime() - self.DamageTick >= 250:
                self.RangeDamage()
                self.DamageTick = GLHelper.GetTime()
            if GLHelper.GetTime() - self.PickupTick >= 500:
                self.RangePickup()
                self.PickupTick = GLHelper.GetTime()
            if GLHelper.GetTime() - self.GeneralTick >= 10:
                self.GeneralCheats()
                self.GeneralTick = GLHelper.GetTime()
        else:
            self.ProcessTimeStamp = GLHelper.GetTime() + 1000

    def UpdatePlayerInfo(self):
        if (GLPlayer.IsOnline()):
            self.CharacterInfoNameLabel.SetText("Name: {}".format(GLPlayer.GetName()))
            self.CharacterInfoLevelLabel.SetText("Lv: {}".format(GLPlayer.GetLevel()))
            self.CharacterInfoHPLabel.SetText("HP: {} / {}".format(GLPythonPlayer.GetStatus(6), GLPythonPlayer.GetStatus(5)))
            self.CharacterInfoSPLabel.SetText("SP: {} / {}".format(GLPythonPlayer.GetStatus(8), GLPythonPlayer.GetStatus(7)))
            self.CharacterInfoEXPLabel.SetText("EXP: {} / {}".format(GLPythonPlayer.GetStatus(4), GLPythonPlayer.GetStatus(3)))
            self.CharacterInfoYangLabel.SetText("Yang: {}".format(GLPythonPlayer.GetStatus(11)))

    def UpdatePlayerList(self):
        if (GLPlayer.IsOnline()):
            range = 200
            playerCount = 0
            objectList = GLList.GetObjectList(range)
            myName = GLPlayer.GetName()
            newPlayerList = []
            for obj in objectList:
                if obj['InstanceType'] == 6 and obj['Name'] != myName:
                    newPlayerList.append(obj['Name'])
                    playerCount += 1
            if newPlayerList != self.playerList:
                self.playerList = newPlayerList
                self.PlayerListBox[0].Hide()
                self.PlayerListBox[1].Hide()
                self.PlayerListBox = self.UI.ListBoxEx(self, 140, 50, 200, 100)
                for playerName in self.playerList:
                    item = ui.TextLine()
                    item.SetText(playerName)
                    self.PlayerListBox[1].AppendItem(item)
            self.PlayerListLabel.SetText("There are {} players in the {} distance field!".format(playerCount, range))
        else:
            self.PlayerListBox[1].RemoveAllItems()

    def AttackCloseMob(self):
        if GLPlayer.IsOnline() and self.LevelBotStatus:
            objectList = GLList.GetObjectList(100)
            for obj in objectList:
                if obj['InstanceType'] == 0 and obj['IsDead'] == 0:
                    if GLHelper.IsBlock(GLPlayer.GetPixelPosition(), obj['GetPixelPosition']) == 0:
                        GLPythonPlayer.SetAutoAttackTargetActorID(obj['VirtualID'])
                        break
        
    def RangeDamage(self):
        if GLPlayer.IsOnline() and self.DamageStatus:
            objectList = GLList.GetObjectList(int(self.DamageRangeEdit[1].GetText()))
            count = 0
            for obj in objectList:
                if obj['InstanceType'] == 0 and obj['IsDead'] == 0:
                    if GLHelper.IsBlock(GLPlayer.GetPixelPosition(), obj['GetPixelPosition']) == 0:
                        steps = GLHelper.DivideTwoPointsByDistance(GLPlayer.GetPixelPosition(), obj['GetPixelPosition'], 2000)
                        for step in steps:
                            GLPythonNetworkStream.SendCharacterStatePacket(step['Position'], 0, 0, 0)
                        
                        GLPythonNetworkStream.SendAttackPacket(0, obj['VirtualID'])

                        steps = GLHelper.DivideTwoPointsByDistance(obj['GetPixelPosition'], GLPlayer.GetPixelPosition(), 2000)
                        for step in steps:
                            GLPythonNetworkStream.SendCharacterStatePacket(step['Position'], 0, 0, 0)
                        
                        count +=1
                        if count >= int(self.DamageLimitEdit[1].GetText()):
                            break

    def RangePickup(self):
        if GLPlayer.IsOnline() and self.PickupStatus:
            myName = GLPlayer.GetName()
            groundItemList = GLList.GetGroundItemList(int(self.DamageRangeEdit[1].GetText()))
            value = 0
            for item in groundItemList:
                if item['Owner'] == '' or item['Owner'] == myName:
                    if GLHelper.IsBlock(GLPlayer.GetPixelPosition(), item['Position']) == 0:
                        steps = GLHelper.DivideTwoPointsByDistance(GLPlayer.GetPixelPosition(), item['Position'], 2000)
                        for step in steps:
                            GLPythonNetworkStream.SendCharacterStatePacket(step['Position'], 0, 0, 0)
                        
                        GLPythonNetworkStream.SendItemPickupPacket(item['VID'])

                        steps = GLHelper.DivideTwoPointsByDistance(item['Position'], GLPlayer.GetPixelPosition(), 2000)
                        for step in steps:
                            GLPythonNetworkStream.SendCharacterStatePacket(step['Position'], 0, 0, 0)

                        break
               

    def GeneralCheats(self):
        if GLPlayer.IsOnline() and self.WallHackStatus:
            GLPlayer.SetSkipCollision(1)

        if GLPlayer.IsOnline() and self.MoveSpeedStatus:
            if GLPlayer.IsWalking():
                rotation = GLPlayer.GetRotation()
                speedValue = int(self.MoveSpeedEdit[1].GetText())
                xx = speedValue * math.sin(rotation * 0.017453)
                yy = speedValue * math.cos(rotation * 0.017453)
                myPos = GLPlayer.GetPixelPosition()
                myPos.x = myPos.x + xx
                myPos.y = myPos.y + yy
                if self.WallHackStatus == False and GLHelper.IsBlock(GLPlayer.GetPixelPosition(), myPos) == 1 :
                    return
                else :
                    GLPlayer.SetPixelPosition(myPos)
                    if self.MoveSpeedStateCount == 1:
                        self.MoveSpeedStateCount = 0
                        GLPythonNetworkStream.SendCharacterStatePacket(myPos, rotation, 0, 0)
                    else:
                        GLPythonNetworkStream.SendCharacterStatePacket(myPos, rotation, 1, 0)  
                        self.MoveSpeedStateCount = 1

    def LevelBotFunc(self, arg):
        if arg == 'on':
            self.LevelBotStatus = True
        elif arg == 'off':
            self.LevelBotStatus = False

    def MoveSpeedFunc(self, arg):
        if arg == 'on':
            self.MoveSpeedStatus = True
        elif arg == 'off':
            self.MoveSpeedStatus = False
    
    def WallHackFunc(self, arg):
        if arg == 'on':
            self.WallHackStatus = True
        elif arg == 'off':
            self.WallHackStatus = False
            GLPlayer.SetSkipCollision(0)
    
    def PickupFunc(self):
        if self.PickupButton.GetText() == 'Start Pickup':
            self.PickupStatus = True
            self.PickupButton.SetText('Stop Pickup')
        else:
            self.PickupButton.SetText('Start Pickup')
            self.PickupStatus = False

    def DamageFunc(self):
        if self.DamageButton.GetText() == 'Start Damage':
            self.DamageStatus = True
            self.DamageButton.SetText('Stop Damage')
        else:
            self.DamageButton.SetText('Start Damage')
            self.DamageStatus = False

    def CHChangeFunc(self, ch):
        GLConnect.ManualCHChanger(ch)
    
    def MapChangeFunc(self, map):
        GLPlayer.ChangeMap(map)

class UI:
    def Button(self, parent, buttonName, tooltipText, x, y, func, str):
        button = ui.Button()
        button.SetParent(parent)
        button.SetPosition(x, y)
        if str == "big":
            button.SetUpVisual("d:/ymir work/ui/public/Big_Button_01.sub")
            button.SetOverVisual("d:/ymir work/ui/public/Big_Button_02.sub")
            button.SetDownVisual("d:/ymir work/ui/public/Big_Button_03.sub")
        elif str == "large":
            button.SetUpVisual("d:/ymir work/ui/public/large_Button_01.sub")
            button.SetOverVisual("d:/ymir work/ui/public/large_Button_02.sub")
            button.SetDownVisual("d:/ymir work/ui/public/large_Button_03.sub")
        elif str == "small":
            button.SetUpVisual("d:/ymir work/ui/public/Small_Button_01.sub")
            button.SetOverVisual("d:/ymir work/ui/public/Small_Button_02.sub")
            button.SetDownVisual("d:/ymir work/ui/public/Small_Button_03.sub")
        button.SetText(buttonName)
        button.SetToolTipText(tooltipText)
        button.Show()
        button.SetEvent(func)
        return button

    def ToggleButton(self, parent, buttonName, tooltipText, x, y, funcUp, funcDown, str):
        button = ui.ToggleButton()
        button.SetParent(parent)
        button.SetPosition(x, y)
        if str == "big":
            button.SetUpVisual("d:/ymir work/ui/public/Big_Button_01.sub")
            button.SetOverVisual("d:/ymir work/ui/public/Big_Button_02.sub")
            button.SetDownVisual("d:/ymir work/ui/public/Big_Button_03.sub")
        elif str == "large":
            button.SetUpVisual("d:/ymir work/ui/public/large_Button_01.sub")
            button.SetOverVisual("d:/ymir work/ui/public/large_Button_02.sub")
            button.SetDownVisual("d:/ymir work/ui/public/large_Button_03.sub")
        elif str == "middle":
            button.SetUpVisual("d:/ymir work/ui/public/middle_Button_01.sub")
            button.SetOverVisual("d:/ymir work/ui/public/middle_Button_02.sub")
            button.SetDownVisual("d:/ymir work/ui/public/middle_Button_03.sub")
        elif str == "small":
            button.SetUpVisual("d:/ymir work/ui/public/Small_Button_01.sub")
            button.SetOverVisual("d:/ymir work/ui/public/Small_Button_02.sub")
            button.SetDownVisual("d:/ymir work/ui/public/Small_Button_03.sub")
        button.SetText(buttonName)
        button.SetToolTipText(tooltipText)
        button.Show()
        button.SetToggleUpEvent(funcUp)
        button.SetToggleDownEvent(funcDown)
        return button

    def EditLine(self, parent, editlineText, x, y, width, heigh, max):
        SlotBar = ui.SlotBar()
        SlotBar.SetParent(parent)
        SlotBar.SetSize(width, heigh)
        SlotBar.SetPosition(x, y)
        SlotBar.Show()
        Value = ui.EditLine()
        Value.SetParent(SlotBar)
        Value.SetSize(width, heigh)
        Value.SetPosition(5, 1)
        Value.SetMax(max)
        Value.SetText(editlineText)
        Value.Show()
        return SlotBar, Value

    def Label(self, parent, x, y, text):
        Label = ui.TextLine()
        Label.SetParent(parent)
        Label.SetPosition(x, y)
        Label.SetText(text)
        Label.Show()
        return Label

    def SliderBar(self, parent, sliderPos, func, x, y):
        Slider = ui.SliderBar()
        if parent != None:
            Slider.SetParent(parent)
        Slider.SetPosition(x, y)
        Slider.SetSliderPos(sliderPos / 100)
        Slider.Show()
        Slider.SetEvent(func)
        return Slider

    def ListBoxEx(self, parent, x, y, width, heigh):
        bar = ui.Bar()
        if parent != None:
            bar.SetParent(parent)
        bar.SetPosition(x, y)
        bar.SetSize(width, heigh)
        bar.SetColor(1996488704)
        bar.Show()
        ListBox = ui.ListBoxEx()
        ListBox.SetParent(bar)
        ListBox.SetPosition(0, 0)
        ListBox.SetSize(width, heigh)
        ListBox.SetViewItemCount(heigh / 20)
        ListBox.Show()
        scroll = ui.ScrollBar()
        scroll.SetParent(ListBox)
        scroll.SetPosition(width - 15, 0)
        scroll.SetScrollBarSize(heigh)
        scroll.Show()
        ListBox.SetScrollBar(scroll)
        return (bar, ListBox)

    def CheckBox(self, parent, text, x, y, func):
        checkBox = ui.ToggleButton()
        checkBox.SetParent(parent)
        checkBox.SetPosition(x, y)
        checkBox.SetUpVisual("d:/ymir work/ui/public/Small_Button_01.sub")
        checkBox.SetOverVisual("d:/ymir work/ui/public/Small_Button_02.sub")
        checkBox.SetDownVisual("d:/ymir work/ui/public/Small_Button_03.sub")
        checkBox.SetText(text)
        checkBox.Show()
        checkBox.SetToggleUpEvent(func)
        checkBox.SetToggleDownEvent(func)
        return checkBox


ExampleGui()