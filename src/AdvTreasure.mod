IMPLEMENTATION MODULE AdvTreasure ;


FROM libc IMPORT printf ;
FROM Executive IMPORT GetCurrentProcess, InitSemaphore, SEMAPHORE,
                      Wait, Signal ;
FROM TimerHandler IMPORT Sleep, TicksPerSecond ;

FROM ASCII IMPORT cr ;
FROM StrLib IMPORT StrCopy, StrConCat, StrLen ;
FROM NumberIO IMPORT CardToStr, WriteCard ;

FROM AdvSystem IMPORT MaxNoOfPlayers,
                      ManWeight,
                      Man,
                      TypeOfDeath,
                      Player,
                      PlayerSet,
                      PlayerNo,
                      ArrowArgs,
                      StartPlayer,
                      TimeMinSec,
                      RandomNumber,
                      ClientRead,
                      DefaultWrite,
                      ReadString,
                      NextFreePlayer,
                      IsPlayerActive,
                      AssignOutputTo,
     
                      GetReadAccessToPlayer,
                      GetWriteAccessToPlayer,
                      ReleaseReadAccessToPlayer,
                      ReleaseWriteAccessToPlayer,
     
                      GetReadAccessToDoor,
                      GetWriteAccessToDoor,
                      ReleaseReadAccessToDoor,
                      ReleaseWriteAccessToDoor,
     
                      GetReadAccessToTreasure,
                      GetWriteAccessToTreasure,
                      ReleaseReadAccessToTreasure,
                      ReleaseWriteAccessToTreasure,
     
                      GetAccessToScreen,
                      ReleaseAccessToScreen,
                      GetAccessToScreenNo,
                      ReleaseAccessToScreenNo ;
     
FROM AdvMap IMPORT Treasure, Rooms, DoorStatus, IncPosition,
                   NoOfRoomsToSpring, MaxNoOfTreasures,
                   NoOfRoomsToHideCoal, NoOfRoomsToHideGrenade,
                   ActualNoOfRooms ;

FROM Screen IMPORT Width, Height,
                   ClearScreen,
                   InitScreen,
                   WriteWounds,
                   WriteWeight,
                   WriteString,
                   WriteCommentLine1,
                   WriteCommentLine2,
                   WriteCommentLine3,
                   DelCommentLine1,
                   DelCommentLine2,
                   DelCommentLine3 ;

FROM AdvMath IMPORT MagicKey,
                    CrystalBall,
                    MagicSpring,
                    SackOfCoal1,
                    SackOfCoal2,
                    HotIron,
                    HandGrenade,
                    MagicSword,
                    MagicShoes,
                    SleepPotion,
                    LumpOfIron,
                    TreasTrove,
                    SpeedPotion,
                    MagicShield,
                    VisionChest,

                    UpDateWoundsAndFatigue,
                    DammageByHandGrenade,
                    DammageByHotIron ;


FROM DrawG IMPORT DrawTreasure, EraseTreasure, EraseMan, DrawMan ;
FROM DrawL IMPORT DrawRoom, DrawAllPlayers ;
FROM AdvSound IMPORT Explode ;

FROM AdvUtil IMPORT PointOnWall, GetDoorOnPoint, PointOnTreasure,
                    HideDoor, RandomRoom, PositionInRoom, InitialDisplay,
                    FreeOfPlayersAndTreasure, Dead ;



(* Treasure routines.                                                *)
(*                                                                   *)
(* The treasures are as follows:                                     *)
(*                                                                   *)
(* 1:  Magic Key           - This treasures allows one to make a     *)
(*                           closed door into a secret door          *)
(*                                                                   *)
(* 2:  Crystal Ball        - This treasure allows one to get the     *)
(*                           direction and Room No of the other      *)
(*                           players                                 *)
(*                                                                   *)
(* 3:  Magic Spring        - When Grabbed, it springs one to another *)
(*                           random picked room                      *)
(*                                                                   *)
(* 4:  Sack Of Coal        - When Grabbed, it insists that it must   *)
(*                           be taken to a randomly picked room      *)
(*                           before it can be dropped                *)
(*                                                                   *)
(* 5:  Sack Of Coal        - Ditto                                   *)
(*                                                                   *)
(* 6:  Hot Iron            - Scolds one if picked up                 *)
(*                                                                   *)
(* 7:  Hand Grenade        - If used will blow up whole room in      *)
(*                           25 seconds                              *)
(*                                                                   *)
(* 8:  Magic Sword         - Enables one to fight with ease          *)
(*                                                                   *)
(* 9:  Magic Shoes         - Enable one to run with minimal effort   *)
(*                                                                   *)
(* 10: Sleep Potion        - Makes one fall to sleep for 24 seconds  *)
(*                                                                   *)
(* 11: Lump Of Iron        - When picked up scatters all treasure in *)
(*                           current room.                           *)
(*                                                                   *)
(* 12: Treasure Trove      - Tells one where or who has the          *)
(*                           treasures.                              *)
(*                                                                   *)
(* 13: Speed Potion        - Increases ones responce time.           *)
(*                                                                   *)
(* 14: Magic Shield        - Repels Normal Arrows.                   *)
(*                                                                   *)
(* 15: Vision Chest        - Allows one to see enemies screen.       *)



VAR
   Tmessage         : ARRAY [0..13] OF CHAR ;
   SackOfCoal       : ARRAY [0..1] OF CARDINAL ;
   PinPulled        : SEMAPHORE ;
   PinHasBeenPulled : BOOLEAN ;
   PlayerPulled     : CARDINAL ;


PROCEDURE GetTreasure ;
VAR
   p, r : CARDINAL ;
   died : BOOLEAN ;
   Tno  : CARDINAL ;
BEGIN
   p := PlayerNo() ;
   GetWriteAccessToPlayer ;
   Tno := GetTreasure1(p) ;
   (* Only way so far to die directly from getting treasures.         *)
   died := (Player[p].DeathType=fireball) ;
   r := Player[p].RoomOfMan ;
   ReleaseWriteAccessToPlayer ;
   IF Tno=SleepPotion
   THEN
      Sleep(24*TicksPerSecond)
   END ;
   IF died
   THEN
      Dead(p, r)
   END
END GetTreasure ;


PROCEDURE GetTreasure1 (p: CARDINAL) : CARDINAL ;
VAR
   x, y, d,
   r,
   TreasNo: CARDINAL ;
   ReDraw,
   ok     : BOOLEAN ;
BEGIN
   ReDraw := FALSE ;
   WITH Player[p] DO
      d := Direction ;
      r := RoomOfMan ;
      x := Xman ;
      y := Yman ;
      IncPosition(x, y, d) ;
      GetWriteAccessToTreasure ;
      PointOnTreasure(r, x, y, TreasNo, ok) ;
      IF ok
      THEN
         IF TreasNo>9
         THEN
            Tmessage[12] := '1' ;
            Tmessage[13] := CHR((TreasNo MOD 10)+ORD('0'))
         ELSE
            Tmessage[12] := ' ' ;
            Tmessage[13] := CHR(TreasNo+ORD('0'))
         END ;
         GetAccessToScreenNo(p) ;
         WriteCommentLine1(p, Tmessage) ;
         WriteCommentLine2(p, Treasure[TreasNo].TreasureName) ;
         DelCommentLine3(p) ;
         ReleaseAccessToScreenNo(p) ;
         PickUpTreasure(p, r, TreasNo, x, y, ReDraw)
      ELSE
         GetAccessToScreenNo(p) ;
         WriteCommentLine1(p, 'thou canst') ;
         DelCommentLine2(p) ;
         DelCommentLine3(p) ;
         ReleaseAccessToScreenNo(p)
      END ;
      ReleaseWriteAccessToTreasure ;
      IF ReDraw
      THEN
         InitScreen(p) ;
         DrawRoom
      END
   END ;
   RETURN( TreasNo )
END GetTreasure1 ;


PROCEDURE PickUpTreasure (p, r, TreasNo, tx, ty: CARDINAL ;
                          VAR ReDraw: BOOLEAN) ;
VAR
   tr, i: CARDINAL ;
   ok   : BOOLEAN ;
   a    : ARRAY [0..14] OF CHAR ;
   b    : ARRAY [0..4] OF CHAR ;
BEGIN
   WITH Player[p] DO
      (* Magic Spring CANNOT be Grabbed AND neither can Lump Of Iron *)
      IF (TreasNo#MagicSpring) AND (TreasNo#LumpOfIron)
      THEN
         INC(Weight, Treasure[TreasNo].Tweight) ;
         Treasure[TreasNo].Rm := 0 ; (* No longer in a Room *)
         GetAccessToScreenNo(p) ;
         WriteWeight(p, Weight) ;
         ReleaseAccessToScreenNo(p) ;
         INCL(TreasureOwn, TreasNo)
      END ;
      EXCL(Rooms[r].Treasures, TreasNo) ; (* Room no longer has treasure *)
      EraseTreasure(r, tx, ty) ;

      IF TreasNo=MagicSpring
      THEN
         (* Magic Spring - Springs treasure and player into different      *)
         (*                rooms.                                          *)

         EraseMan(p) ;
         REPEAT
            RandomNumber(r, ActualNoOfRooms) ;  (* r>=0 & r<=ActualNoOfRooms-1 *)
            INC(r) ;
            RandomRoom(r, NoOfRoomsToSpring, tr) ;
            PositionInRoom(tr, tx, ty, ok)
         UNTIL ok ;
         RoomOfMan := tr ;
         Xman := tx ;
         Yman := ty ;
         ScreenX := tx-(tx MOD Width) ;
         ScreenY := ty-(ty MOD Height) ;
         DrawMan(p) ;
         REPEAT
            RandomNumber(r, ActualNoOfRooms) ;
            INC(r) ;
            RandomRoom(r, NoOfRoomsToSpring, tr) ;
            PositionInRoom(tr, tx, ty, ok)
         UNTIL ok ;
         WITH Treasure[TreasNo] DO
            Rm := tr ;
            Xpos := tx ;
            Ypos := ty
         END ;
         INCL(Rooms[tr].Treasures, TreasNo) ; (* Room has treasure *)
         DrawTreasure(tr, tx, ty) ;
         ReDraw := TRUE

      ELSIF (TreasNo=SackOfCoal1) OR (TreasNo=SackOfCoal2)  (* Sacks Of Coal *)
      THEN
         RandomNumber(r, ActualNoOfRooms) ;
         INC(r) ;
         RandomRoom(r, NoOfRoomsToHideCoal, tr) ;
         SackOfCoal[TreasNo-SackOfCoal1] := tr ;
         StrCopy('to room ', a ) ;
         CardToStr(tr, 4, b) ;
         StrConCat(a, b, a) ;
         GetAccessToScreenNo(p) ;
         WriteCommentLine3(p, a) ;
         ReleaseAccessToScreenNo(p)
      ELSIF TreasNo=HotIron             (* Hot iron      *)
      THEN
         GetAccessToScreenNo(p) ;
         WriteCommentLine1(p, 'ouch') ;
         WriteCommentLine2(p, 'fire ball') ;
         WriteCommentLine3(p, 'hit thee') ;
         IF DammageByHotIron>Wounds
         THEN
            Wounds := 0 ;
            DeathType := fireball
         ELSE
            DEC(Wounds, DammageByHotIron)
         END ;
         WriteWounds(p, Wounds) ;
         ReleaseAccessToScreenNo(p)
      ELSIF TreasNo=LumpOfIron
      THEN
         ScatterAllTreasures(p, RoomOfMan)
      ELSIF TreasNo=SpeedPotion
      THEN
         (* PutPriority(CurrentProcess, User, 4) *)
      END
   END
END PickUpTreasure ;


PROCEDURE ScatterAllTreasures (p, r: CARDINAL) ;
VAR
   s       : INTEGER ;
   tp, tr,
   x, y, i : CARDINAL ;
   ok      : BOOLEAN ;
BEGIN
   FOR i := 1 TO MaxNoOfTreasures DO
      FOR tp := 0 TO NextFreePlayer-1 DO
         IF IsPlayerActive(tp)
         THEN
            WITH Player[tp] DO
               IF (i IN TreasureOwn) AND (r=RoomOfMan)
               THEN
                  REPEAT
                     RandomRoom(r, NoOfRoomsToSpring, tr) ;
                     PositionInRoom(tr, x, y, ok)
                  UNTIL ok ;
                  WITH Treasure[i] DO
                     DEC(Weight, Tweight) ;
                     Xpos := x ;
                     Ypos := y ;
                     Rm := tr
                  END ;
                  s := printf("treasure %d is in room %d at %d,%d\n", i, tr, x, y) ;
                  INCL(Rooms[tr].Treasures, i)
               END
            END
         END
      END ;
      IF Treasure[i].Rm=r
      THEN
         REPEAT
            RandomRoom(r, NoOfRoomsToSpring, tr) ;
            PositionInRoom(tr, x, y, ok)
         UNTIL ok ;
         s := printf("treasure %d is in room %d at %d,%d\n", i, tr, x, y) ;
         WITH Treasure[i] DO
            EraseTreasure(Rm, Xpos, Ypos) ;
            EXCL(Rooms[Rm].Treasures, i) ;
            Xpos := x ;
            Ypos := y ;
            Rm := tr
         END ;
         INCL(Rooms[tr].Treasures, i)
      END ;
      WITH Treasure[i] DO
         DrawTreasure(Rm, Xpos, Ypos)
      END
   END ;
   FOR tp := 0 TO NextFreePlayer-1 DO
      IF IsPlayerActive(tp)
      THEN
         WITH Player[tp] DO
            IF (TreasureOwn#{}) AND (RoomOfMan=r)
            THEN
               (* Now undo treasures which have an automatic effect *)
               IF SpeedPotion IN TreasureOwn
               THEN
                  (* PutPriority(PlayerProcess(p), User, 3) *)
               END ;

               TreasureOwn := {} ;
               GetAccessToScreenNo(tp) ;

               WriteWeight(p, Weight) ;
               WriteCommentLine1(p, 'thy burdens') ;
               WriteCommentLine2(p, 'hast been') ;
               WriteCommentLine3(p, 'lifted') ;

               ReleaseAccessToScreenNo(tp)
            END
         END
      END
   END
END ScatterAllTreasures ;   


PROCEDURE ScatterTreasures (p, r: CARDINAL) ;
VAR
   c       : INTEGER ;
   x, y, i : CARDINAL ;
   ok      : BOOLEAN ;
BEGIN
   WITH Player[p] DO
      FOR i := 1 TO MaxNoOfTreasures DO
         IF i IN TreasureOwn
         THEN
            (* Now undo treasures which have an automatic effect *)
            IF SpeedPotion IN TreasureOwn
            THEN
               (* PutPriority(PlayerProcess(p), User, 3) *)
            END ;

            REPEAT
               PositionInRoom(r, x, y, ok) ;
               IF ok
               THEN
                  WITH Treasure[i] DO
                     DEC(Weight, Tweight) ;
                     Xpos := x ;
                     Ypos := y ;
                     Rm := r
                  END ;
                  DrawTreasure(r, x, y) ;
                  INCL(Rooms[r].Treasures, i) ;
               ELSE
                  c := printf('trying another room\n') ;
                  RandomRoom(r, 1, x) ;
                  r := x
               END
            UNTIL ok
         END
      END ;
      TreasureOwn := {} ;
      GetAccessToScreenNo(p) ;
      WriteWeight(p, Weight) ;
      ReleaseAccessToScreenNo(p)
   END
END ScatterTreasures ;


PROCEDURE DropTreasure ;
VAR
   ok        : BOOLEAN ;
   p, TreasNo: CARDINAL ;
   ch,
   units,
   tens      : CHAR ;
BEGIN
   p := PlayerNo() ;
   GetAccessToScreenNo(p) ;
   WriteCommentLine2(p, 'which one?') ;
   ReleaseAccessToScreenNo(p) ;
   ch := ' ' ;
   units := ' ' ;
   tens := ' ' ;
   REPEAT
      tens := units ;
      units := ch ;
      ok := ClientRead(ch)
   UNTIL (NOT ok) OR (ch=cr) ;
   IF ok
   THEN
      IF (units>='0') AND (units<='9')
      THEN
         TreasNo := ORD(units)-ORD('0') ;
         IF (tens>='0') AND (tens<='9')
         THEN
            TreasNo := TreasNo+10*(ORD(tens)-ORD('0'))
         END
      END ;
      IF (TreasNo<1) OR (TreasNo>MaxNoOfTreasures)
      THEN
         GetAccessToScreenNo(p) ;
         WriteCommentLine1(p, 'thou canst') ;
         DelCommentLine2(p) ;
         DelCommentLine3(p);
         ReleaseAccessToScreenNo(p)
      ELSE
         GetWriteAccessToPlayer ;
         DropTreasure1(p, TreasNo) ;
         ReleaseWriteAccessToPlayer
      END
   END
END DropTreasure ;


PROCEDURE DropTreasure1(p, TreasNo: CARDINAL) ;
VAR
   x, y, d,
   r, z   : CARDINAL ;
   ok     : BOOLEAN ;
BEGIN
   WITH Player[p] DO
      IF TreasNo IN TreasureOwn
      THEN
         d := Direction ;
         r := RoomOfMan ;
         x := Xman ;
         y := Yman ;
         IncPosition(x, y, d) ;
         PointOnWall(r, x, y, ok) ;
         IF NOT ok
         THEN
            GetDoorOnPoint(r, x, y, z, ok) ;
            IF NOT ok
            THEN
               GetWriteAccessToTreasure ;
               FreeOfPlayersAndTreasure(r, x, y, ok) ;
               IF ok
               THEN
                  IF TreasNo>9
                  THEN
                     Tmessage[12] := '1' ;
                     Tmessage[13] := CHR((TreasNo MOD 10)+ORD('0'))
                  ELSE
                     Tmessage[12] := ' ' ;
                     Tmessage[13] := CHR(TreasNo+ORD('0'))
                  END ;
                  GetAccessToScreenNo(p) ;
                  WriteCommentLine1(p, Tmessage) ;
                  WriteCommentLine2(p, Treasure[TreasNo].TreasureName) ;
                  ReleaseAccessToScreenNo( p ) ;
                  PutDownTreasure(p, r, TreasNo, x, y)
               ELSE
                  GetAccessToScreenNo(p) ;
                  WriteCommentLine1(p, 'thou canst') ;
                  DelCommentLine2(p) ;
                  DelCommentLine3(p) ;
                  ReleaseAccessToScreenNo(p)
               END ;
               ReleaseWriteAccessToTreasure
            ELSE
               GetAccessToScreenNo(p) ;
               WriteCommentLine1(p, 'thou canst') ;
               DelCommentLine2(p) ;
               DelCommentLine3(p) ;
               ReleaseAccessToScreenNo(p)
            END
         ELSE
            GetAccessToScreenNo(p) ;
            WriteCommentLine1(p, 'thou canst') ;
            DelCommentLine2(p) ;
            DelCommentLine3(p) ;
            ReleaseAccessToScreenNo(p)
         END
      ELSE
         GetAccessToScreenNo(p) ;
         WriteCommentLine1(p, 'thou canst') ;
         DelCommentLine2(p) ;
         DelCommentLine3(p) ;
         ReleaseAccessToScreenNo(p)
      END
   END
END DropTreasure1 ;


PROCEDURE PutDownTreasure(p, r, TreasNo, tx, ty: CARDINAL) ;
VAR
   tr, i: CARDINAL ;
   ok   : BOOLEAN ;
   a    : ARRAY [0..14] OF CHAR ;
   b    : ARRAY [0..4] OF CHAR ;
BEGIN
   WITH Player[p] DO
      IF (TreasNo=SackOfCoal1) OR (TreasNo=SackOfCoal2)  (* Sacks Of Coal *)
      THEN
         IF r=SackOfCoal[TreasNo-SackOfCoal1]
         THEN
            DEC(Weight, Treasure[TreasNo].Tweight) ;
            Treasure[TreasNo].Rm := r ;    (* Put in this Room *)
            Treasure[TreasNo].Xpos := tx ;
            Treasure[TreasNo].Ypos := ty ;
            GetAccessToScreenNo(p) ;
            WriteWeight(p, Weight) ;
            WriteCommentLine3(p, 'dropped') ;
            ReleaseAccessToScreenNo(p) ;
            INCL(Rooms[r].Treasures, TreasNo) ; (* Room has treasure             *)
            EXCL(TreasureOwn, TreasNo) ;  (* Player no longer has treasure *)
            DrawTreasure(r, tx, ty)
         ELSE
            StrCopy('to room ', a) ;
            CardToStr(SackOfCoal[TreasNo-SackOfCoal1], 4, b) ;
            StrConCat(a, b, a) ;
            GetAccessToScreenNo(p) ;
            WriteCommentLine3(p, a) ;
            ReleaseAccessToScreenNo(p)
         END
      ELSE
         IF TreasNo=SpeedPotion
         THEN
            (* PutPriority(CurrentProcess, User, 3) *)
         END ;
         DEC(Weight, Treasure[TreasNo].Tweight) ;
         Treasure[TreasNo].Rm := r ;    (* Put in this Room *)
         Treasure[TreasNo].Xpos := tx ;
         Treasure[TreasNo].Ypos := ty ;
         GetAccessToScreenNo(p) ;
         WriteCommentLine3(p, 'dropped') ;
         WriteWeight(p, Weight) ;
         ReleaseAccessToScreenNo(p) ;
         INCL(Rooms[r].Treasures, TreasNo) ; (* Room has treasure             *)
         EXCL(TreasureOwn, TreasNo) ;  (* Player no longer has treasure *)
         DrawTreasure(r, tx, ty)
      END
   END
END PutDownTreasure ;


PROCEDURE UseTreasure ;
VAR
   x, y, d,
   r, p,
   TreasNo: CARDINAL ;
   ok     : BOOLEAN ;
   ch,
   units,
   tens   : CHAR ;
BEGIN
   p := PlayerNo() ;
   WITH Player[p] DO
      GetAccessToScreenNo(p) ;
      WriteCommentLine2(p, 'which one?') ;
      ReleaseAccessToScreenNo(p) ;
      ch := ' ' ;
      units := ' ' ;
      tens := ' ' ;
      REPEAT
         tens := units ;
         units := ch ;
         ok := ClientRead(ch)
      UNTIL (NOT ok) OR (ch=cr) ;
      IF ok
      THEN
         IF (units>='0') AND (units<='9')
         THEN
            TreasNo := ORD(units)-ORD('0') ;
            IF (tens>='0') AND (tens<='9')
            THEN
               TreasNo := TreasNo+10*(ORD(tens)-ORD('0'))
            END
         END ;
         GetReadAccessToPlayer ;
         IF (TreasNo<1) OR (TreasNo>MaxNoOfTreasures)
         THEN
            ReleaseReadAccessToPlayer ;
            GetAccessToScreenNo(p) ;
            WriteCommentLine1(p, 'thou canst') ;
            DelCommentLine2(p) ;
            DelCommentLine3(p) ;
            ReleaseAccessToScreenNo(p)
         ELSIF TreasNo IN TreasureOwn
         THEN
            ReleaseReadAccessToPlayer ;
            IF TreasNo>9
            THEN
               Tmessage[12] := tens ;
               Tmessage[13] := units
            ELSE
               Tmessage[12] := ' ' ;
               Tmessage[13] := units
            END ;
            GetAccessToScreenNo(p) ;
            WriteCommentLine1(p, 'using') ;
            WriteCommentLine2(p, Tmessage) ;
            WriteCommentLine3(p, Treasure[TreasNo].TreasureName) ;
            ReleaseAccessToScreenNo(p) ;
            IF TreasNo=MagicKey        (* Magic Key *)
            THEN
               HideDoor
            ELSIF TreasNo=CrystalBall  (* Crystal Ball *)
            THEN
               UseCrystalBall
            ELSIF TreasNo=HandGrenade  (* Hand Grenade *)
            THEN
               PullPin
            ELSIF TreasNo=TreasTrove
            THEN
               DisplayTreasures
            ELSIF TreasNo=VisionChest
            THEN
               DisplayEnemy
            END
         ELSE
            ReleaseReadAccessToPlayer ;
            GetAccessToScreenNo(p) ;
            WriteCommentLine1(p, 'thou canst') ;
            DelCommentLine2(p) ;
            DelCommentLine3(p) ;
            ReleaseAccessToScreenNo(p)
         END
      END
   END
END UseTreasure ;


PROCEDURE UseCrystalBall ;
VAR
   p, x, y,
   px, py,
   r, i : CARDINAL ;
   a    : ARRAY [0..14] OF CHAR ;
   b    : ARRAY [0..4]  OF CHAR ;
   who  : ARRAY [0..1] OF CARDINAL ;
   first: BOOLEAN ;
   ch   : CHAR ;
BEGIN
(*
   p := PlayerNo() ;
   first := TRUE ;
   FOR i := 0 TO MaxNoOfPlayers DO
      IF i#p
      THEN
         IF first
         THEN
            who[0] := i ;
            first := FALSE
         ELSE
            who[1] := i
         END
      END
   END ;
   GetReadAccessToPlayerNo( p ) ;
   WITH Player[p] DO
      px := Xman ;
      py := Yman
   END ;
   ReleaseReadAccessToPlayerNo( p ) ;
   GetReadAccessToPlayerNo( who[0] ) ;
   StrConCat('1: ', Player[who[0]].ManName, a ) ;
   ReleaseReadAccessToPlayerNo( who[0] ) ;
   GetAccessToScreenNo( p ) ;
   WriteCommentLine1(p, a) ;
   ReleaseAccessToScreenNo( p ) ;
   GetReadAccessToPlayerNo( who[1] ) ;
   StrConCat('2: ', Player[who[1]].ManName, a ) ;
   ReleaseReadAccessToPlayerNo( who[1] ) ;
   GetAccessToScreenNo( p ) ;
   WriteCommentLine2(p, a) ;
   WriteCommentLine3(p, 'peer at ?') ;
   ReleaseAccessToScreenNo( p ) ;
   REPEAT
      Read( ch ) ;
      IF (ch='1') OR (ch='2')
      THEN
         i := ORD(ch)-ORD('1') ;
         GetReadAccessToPlayerNo( who[i] ) ;
         WITH Player[who[i]] DO
            x := Xman ;
            y := Yman ; 
            r := RoomOfMan
         END ;
         ReleaseReadAccessToPlayerNo( who[i] ) ;
         IF r=0
         THEN
            StrCopy('is slain: ', a )
         ELSE
            StrCopy('room', a) ;
            CardToStr( r, 4, b ) ;
            StrConCat( a, b, a ) ;
            StrConCat( a, ' ', a )
         END ;
         IF y>py
         THEN
            StrConCat( a, 'S', a )
         END ;
         IF y<py
         THEN
            StrConCat( a, 'N', a )
         END ;
         IF x>px
         THEN
            StrConCat( a, 'E', a )
         END ;
         IF x<px
         THEN
            StrConCat( a, 'W', a )
         END ;
         GetAccessToScreenNo( p ) ;
         IF ch='1'
         THEN
            WriteCommentLine1(p, a)
         ELSE
            WriteCommentLine2(p, a)
         END ;
         ReleaseAccessToScreenNo( p )
      END
   UNTIL (ch#'1') AND (ch#'2') ;
   GetAccessToScreenNo( p ) ;
   DelCommentLine1(p) ;
   DelCommentLine2(p) ;
   DelCommentLine3(p) ;
   ReleaseAccessToScreenNo( p )
*)
END UseCrystalBall ;

(*
PROCEDURE DisplayWounds ;
VAR
   p, w,
   r, i : CARDINAL ;
   b    : ARRAY [0..4]  OF CHAR ;
   a    : ARRAY [0..14] OF CHAR ;
   who  : ARRAY [0..1] OF CARDINAL ;
   first: BOOLEAN ;
   ch   : CHAR ;
BEGIN
   p := PlayerNo() ;
   first := TRUE ;
   FOR i := 0 TO MaxNoOfPlayers DO
      IF i#p
      THEN
         IF first
         THEN
            who[0] := i ;
            first := FALSE
         ELSE
            who[1] := i
         END
      END
   END ;
   GetReadAccessToPlayerNo( who[0] ) ;
   StrConCat('1: ', Player[who[0]].ManName, a ) ;
   ReleaseReadAccessToPlayerNo( who[0] ) ;
   GetAccessToScreenNo( p ) ;
   WriteCommentLine1(p, a) ;
   ReleaseAccessToScreenNo( p ) ;
   GetReadAccessToPlayerNo( who[1] ) ;
   StrConCat('2: ', Player[who[1]].ManName, a ) ;
   ReleaseReadAccessToPlayerNo( who[1] ) ;
   GetAccessToScreenNo( p ) ;
   WriteCommentLine2(p, a) ;
   WriteCommentLine3(p, 'peer at ?') ;
   ReleaseAccessToScreenNo( p ) ;
   REPEAT
      Read( ch ) ;
      IF (ch='1') OR (ch='2')
      THEN
         i := ORD(ch)-ORD('1') ;
         GetReadAccessToPlayerNo( who[i] ) ;
         WITH Player[who[i]] DO
            w := Wounds ;
            r := RoomOfMan
         END ;
         ReleaseReadAccessToPlayerNo( who[i] ) ;
         IF r=0
         THEN
            StrCopy('is slain: ', a )
         ELSE
            StrCopy('Wounds ', a) ;
            CardToStr( w, 4, b ) ;
            StrConCat( a, b, a ) ;
            StrConCat( a, ' ', a )
         END ;
         GetAccessToScreenNo( p ) ;
         IF ch='1'
         THEN
            WriteCommentLine1(p, a)
         ELSE
            WriteCommentLine2(p, a)
         END ;
         ReleaseAccessToScreenNo( p )
      END
   UNTIL (ch#'1') AND (ch#'2') ;
   GetAccessToScreenNo( p ) ;
   DelCommentLine1(p) ;
   DelCommentLine2(p) ;
   DelCommentLine3(p) ;
   ReleaseAccessToScreenNo( p )
END DisplayWounds ;
*)

PROCEDURE DisplayEnemy ;
VAR
   p,
   r, i : CARDINAL ;
   who  : ARRAY [0..1] OF CARDINAL ;
   a    : ARRAY [0..14] OF CHAR ;
   first: BOOLEAN ;
   ch   : CHAR ;
BEGIN
(*
   p := PlayerNo() ;
   first := TRUE ;
   FOR i := 0 TO MaxNoOfPlayers DO
      IF i#p
      THEN
         IF first
         THEN
            who[0] := i ;
            first := FALSE
         ELSE
            who[1] := i
         END
      END
   END ;
   REPEAT
      GetReadAccessToPlayerNo( who[0] ) ;
      StrConCat('1: ', Player[who[0]].ManName, a ) ;
      ReleaseReadAccessToPlayerNo( who[0] ) ;
      GetAccessToScreenNo( p ) ;
      WriteCommentLine1(p, a) ;
      ReleaseAccessToScreenNo( p ) ;
      GetReadAccessToPlayerNo( who[1] ) ;
      StrConCat('2: ', Player[who[1]].ManName, a ) ;
      ReleaseReadAccessToPlayerNo( who[1] ) ;
      GetAccessToScreenNo( p ) ;
      WriteCommentLine2(p, a) ;
      WriteCommentLine3(p, 'peer at ?') ;
      ReleaseAccessToScreenNo( p ) ;
      Read( ch ) ;
      IF (ch='1') OR (ch='2')
      THEN
         i := ORD(ch)-ORD('1') ;
         GetReadAccessToPlayerNo( who[i] ) ;
         WITH Player[who[i]] DO
            r := RoomOfMan
         END ;
         ReleaseReadAccessToPlayerNo( who[i] ) ;
         IF r=0
         THEN
            GetAccessToScreenNo( p ) ;
            IF ch='1'
            THEN
               WriteCommentLine1(p, 'is slain:')
            ELSE
               WriteCommentLine2(p, 'is slain:')
            END ;
            ReleaseAccessToScreenNo( p )
         ELSE
            DisplayEn( p, who[i] )
         END
      END
   UNTIL (ch#'1') AND (ch#'2') ;
   GetAccessToScreenNo( p ) ;
   DelCommentLine1(p) ;
   DelCommentLine2(p) ;
   DelCommentLine3(p) ;
   ReleaseAccessToScreenNo( p )
*)
END DisplayEnemy ;


PROCEDURE DisplayEn (p, e: CARDINAL) ;
VAR
   OldMan: Man ;
   ch    : CHAR ;
BEGIN
(* ******************
   (* Save player p man first *)
   GetWriteAccessToAllPlayers ;
   OldMan := Player[p] ;
   Player[p] := Player[e] ;
   (* Now draw Screen etc *)
   InitScreen ;
   DrawRoom ;
   DrawAllPlayers ;
   Player[p] := OldMan ;
   ReleaseWriteAccessToAllPlayers ;
   Read( ch ) ;
   IF Player[p].RoomOfMan#0   (* So alive - or just killed hopefully... *)
   THEN
      InitialDisplay
   END
********************** *)
END DisplayEn ;


PROCEDURE DisplayTreasures ;
VAR
   p, tp,
   i, j : CARDINAL ;
   ok   : BOOLEAN ;
   ch   : CHAR ;
   no   : ARRAY [0..3] OF CHAR ;
   line : ARRAY [0..80] OF CHAR ;
BEGIN
   p := PlayerNo() ;
   GetReadAccessToPlayer ;
   GetReadAccessToTreasure ;
   GetAccessToScreenNo(p) ;
   ClearScreen(p) ;
   FOR i := 1 TO MaxNoOfTreasures DO
      ok := FALSE ;
      FOR tp := 0 TO MaxNoOfPlayers DO
         IF IsPlayerActive(tp)
         THEN
            WITH Player[tp] DO
               IF i IN TreasureOwn
               THEN
                  StrCopy(ManName, line) ;
                  StrConCat(line, ' ', line) ;
                  ok := TRUE
               END
            END
         END
      END ;
      IF NOT ok
      THEN
         CardToStr(Treasure[i].Rm, 6, line) ;
         StrConCat(' ', line, line) ;
         StrConCat('Room Number', line, line) ;
      END ;
      StrConCat(line, ' has Treasure No ', line) ;
      CardToStr(i, 0, no) ;
      StrConCat(line, no, line) ;
      StrConCat(line, ' the ', line) ;
      (* wrong before here *)
      StrConCat(line, Treasure[i].TreasureName, line) ;
      WriteString(p, line)
   END ;
   ReleaseReadAccessToPlayer ;
   ReleaseReadAccessToTreasure ;
   ReleaseAccessToScreenNo(p) ;
   IF ClientRead(ch)
   THEN
   END ;
   InitialDisplay
END DisplayTreasures ;


PROCEDURE PullPin ;
VAR
   p: CARDINAL ;
BEGIN
   p := PlayerNo() ;
   GetWriteAccessToTreasure ;
   IF PinHasBeenPulled
   THEN
      ReleaseWriteAccessToTreasure ;
      GetAccessToScreen ;
      WriteCommentLine1(p, 'pin has been') ;
      WriteCommentLine2(p, 'pulled') ;
      DelCommentLine3(p) ;
      ReleaseAccessToScreen
   ELSE
      PinHasBeenPulled := TRUE ;
      PlayerPulled := p ;
      ReleaseWriteAccessToTreasure ;
      Signal(PinPulled)
   END
END PullPin ;


PROCEDURE Grenade ;
VAR
   pulled,
   RoomOfExplosion,
   sec, i,
   start : CARDINAL ;
   hit,
   ok    : BOOLEAN ;
   SlainP: PlayerSet ;
BEGIN
   LOOP
      Wait(PinPulled) ;
      pulled := PlayerPulled ;
      Sleep(25*TicksPerSecond) ;

      (* Ok now explode! *)

      hit := FALSE ;
      GetWriteAccessToPlayer ;
      GetWriteAccessToTreasure ;

      (* Find out where grenade is! *)

      WITH Treasure[HandGrenade] DO
         IF Rm=0
         THEN
            i := 0 ;
            RoomOfExplosion := 0 ;
            REPEAT
               IF IsPlayerActive(i)
               THEN
                  WITH Player[i] DO
                     IF HandGrenade IN TreasureOwn
                     THEN
                        RoomOfExplosion := RoomOfMan ;
                        DEC(Weight, Tweight) ;
                        EXCL(TreasureOwn, HandGrenade) ;
                        GetAccessToScreenNo(i) ;
                        WriteWeight(i, Weight) ;
                        ReleaseAccessToScreenNo(i)
                     END
                  END
               END ;
               INC(i)
            UNTIL RoomOfExplosion#0 ;
         ELSE
            RoomOfExplosion := Rm ;
            EXCL(Rooms[Rm].Treasures, HandGrenade) ;
            EraseTreasure(Rm, Xpos, Ypos)
         END
      END ;

      SlainP := PlayerSet{} ;
      FOR i := 0 TO NextFreePlayer-1 DO
         IF IsPlayerActive(i)
         THEN
            WITH Player[i] DO
               IF RoomOfExplosion=RoomOfMan
               THEN
                  hit := TRUE ;
                  GetAccessToScreenNo(i) ;
                  UpDateWoundsAndFatigue(i) ;
                  WriteCommentLine1(i, 'boooommm') ;
                  DelCommentLine2(i) ;
                  DelCommentLine3(i) ;
                  IF Wounds>DammageByHandGrenade
                  THEN
                     DEC(Wounds, DammageByHandGrenade) ;
                  ELSE
                     INCL(SlainP, i) ;
                     Wounds := 0 ;
                     DeathType := explosion
                  END ;
                  WriteWounds(i, Wounds) ;
                  ReleaseAccessToScreenNo(i)
               END
            END
         END
      END ;
      WITH Treasure[HandGrenade] DO
         REPEAT
            RandomRoom(RoomOfExplosion, NoOfRoomsToHideGrenade, Rm) ;
            PositionInRoom(Rm, Xpos, Ypos, ok)
         UNTIL ok ;
         INCL(Rooms[Rm].Treasures, HandGrenade) ;
         DrawTreasure(Rm, Xpos, Ypos)
      END ;
      PinHasBeenPulled := FALSE ;
      ReleaseWriteAccessToTreasure ;
      ReleaseWriteAccessToPlayer ;
      Explode(RoomOfExplosion, pulled, hit) ;
      FOR i := 0 TO MaxNoOfPlayers DO
         IF i IN SlainP
         THEN
            Dead(i, RoomOfExplosion)
         END
      END
   END
END Grenade ;


PROCEDURE Init ;
BEGIN
   PinPulled := InitSemaphore(0, 'PinPulled') ;
   PinHasBeenPulled := FALSE ;

   StrCopy('Magic Key'   , Treasure[MagicKey   ].TreasureName ) ;
   StrCopy('Crystal Ball', Treasure[CrystalBall].TreasureName ) ;
   StrCopy('Magic Spring', Treasure[MagicSpring].TreasureName ) ;
   StrCopy('Sack Of Coal', Treasure[SackOfCoal1].TreasureName ) ;
   StrCopy('Sack Of Coal', Treasure[SackOfCoal2].TreasureName ) ;
   StrCopy('Hot Iron'    , Treasure[HotIron    ].TreasureName ) ;
   StrCopy('Hand Grenade', Treasure[HandGrenade].TreasureName ) ;
   StrCopy('Magic Sword' , Treasure[MagicSword ].TreasureName ) ;
   StrCopy('Magic Shoes' , Treasure[MagicShoes ].TreasureName ) ;
   StrCopy('Sleep Potion', Treasure[SleepPotion].TreasureName ) ;
   StrCopy('Lump Of Iron', Treasure[LumpOfIron ].TreasureName ) ;
   StrCopy('Treas. Trove', Treasure[TreasTrove ].TreasureName ) ;
   StrCopy('Speed Potion', Treasure[SpeedPotion].TreasureName ) ;
   StrCopy('Magic Shield', Treasure[MagicShield].TreasureName ) ;
   StrCopy('Vision Chest', Treasure[VisionChest].TreasureName ) ;

   Treasure[MagicKey   ].Tweight :=   0 ;   (* Was   0 *)
   Treasure[CrystalBall].Tweight :=  33 ;   (* Was  43 *)
   Treasure[MagicSpring].Tweight :=   0 ;   (* Was   0 *)
   Treasure[SackOfCoal1].Tweight := 150 ;   (* Was 200 *)
   Treasure[SackOfCoal2].Tweight := 150 ;   (* Was 200 *)
   Treasure[HotIron    ].Tweight :=   4 ;   (* Was   4 *)
   Treasure[HandGrenade].Tweight :=   3 ;   (* Was   3 *)
   Treasure[MagicSword ].Tweight :=   1 ;   (* Was   1 *)
   Treasure[MagicShoes ].Tweight :=   0 ;   (* Was   0 *)
   Treasure[SleepPotion].Tweight :=   5 ;   (* Was   5 *)
   Treasure[LumpOfIron ].Tweight :=   0 ;   (* Was   0 *)
   Treasure[TreasTrove ].Tweight :=  53 ;   (* Was  43 *)
   Treasure[SpeedPotion].Tweight :=   0 ;   (* Was   0 *)
   Treasure[MagicShield].Tweight :=   2 ;   (* Was   2 *)
   Treasure[VisionChest].Tweight := 120 ;   (* Was 150 *)

   StrCopy('Treasure No xx', Tmessage )
END Init ;


BEGIN
   Init
END AdvTreasure.
(*
 * Local variables:
 *  compile-command: "make"
 * End:
 *)
