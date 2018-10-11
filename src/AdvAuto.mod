IMPLEMENTATION MODULE AdvAuto ;



FROM StdIO IMPORT ProcRead, Write ;

FROM StrIO IMPORT ReadString, WriteString, WriteLn ;

FROM AdvSystem IMPORT Player, PlayerNo, MaxNoOfPlayers,
                      GetWriteAccessToAllPlayers,
                      ReleaseWriteAccessToAllPlayers,
                      GetReadAccessToAllPlayers,
                      ReleaseReadAccessToAllPlayers,
                      GetWriteAccessToPlayerNo,
                      ReleaseWriteAccessToPlayerNo,
                      GetReadAccessToPlayerNo,
                      ReleaseReadAccessToPlayerNo,
                      GetReadAccessToTreasure,
                      ReleaseReadAccessToTreasure,
                      GetAccessToScreenNo,
                      ReleaseAccessToScreenNo,
                      TypeOfDeath,
                      ManWeight ;

FROM AdvMap IMPORT IncPosition ;

FROM AdvUtil IMPORT PointOnTreasure, PointOnWall,
                    TestIfLastLivePlayer, PositionInRoom,
                    InitialDisplay ;

FROM AdvMath IMPORT RequiredToAttack,
                    RequiredToFireMagic,
                    RequiredToFireArrow,
                    MagicShield ;

FROM Screen IMPORT Width, Height ;

FROM DrawG IMPORT DrawMan, EraseMan ;

FROM StrLib IMPORT StrLen ;

FROM Kernel IMPORT CurrentProcess, Sleep, Awaited, ClockFreq ;

FROM IO IMPORT STREAM ;

FROM ASCII IMPORT cr ;



CONST
   MaxBufferSize = 80 ;


TYPE
   Buffer     = RECORD
                   buf : ARRAY [0..MaxBufferSize-1] OF CHAR ;
                   in  : CARDINAL ;
                   out : CARDINAL ;
                   no  : CARDINAL ;
                END ;


VAR
   ManBuffer  : ARRAY [0..MaxNoOfPlayers] OF Buffer ;
   ManRead    : ARRAY [0..MaxNoOfPlayers] OF ProcRead ;
   Robot      : ARRAY [0..MaxNoOfPlayers] OF BOOLEAN ;



PROCEDURE StartAuto ;
VAR
   p: CARDINAL ;
BEGIN
   p := PlayerNo() ;
   WriteLn ;
   WriteLn ;
   WriteLn ;
   WriteString('Enter thy name of ghost: ') ;
   ReadString( CurrentProcess^.PName ) ;
   WriteLn ;
   GetWriteAccessToPlayerNo( p ) ;
   GetAccessToScreenNo( p ) ;
   InitBuffer ;
   ManRead[p] := CurrentProcess^.PStream^.inchar ;
   Robot[p] := TRUE ;
   CurrentProcess^.PStream^.inchar := Auto ;
   ReleaseAccessToScreenNo( p ) ;
   ReleaseWriteAccessToPlayerNo( p ) ;
   PutStr( CurrentProcess^.PName ) ;
   PutChar( cr )
END StartAuto ;


PROCEDURE Auto (VAR ch: CHAR) ;
VAR
   p: CARDINAL ;
BEGIN
   p := PlayerNo() ;
   IF Empty()
   THEN
      GetCmd( p )
   END ;
   GetChar( ch )
END Auto ;


PROCEDURE GetCmd (p: CARDINAL) ;
VAR
   done: BOOLEAN ;
BEGIN
   REPEAT
      done := Finish(p) ;
      IF NOT done
      THEN
         IF TooTired(p)
         THEN
            done := Rest(p)
         ELSE
            done := Fight(p) ;
            IF NOT done
            THEN
               done := DodgeArrows(p) OR Move(p) OR (NOT Empty()) ;
               IF NOT done
               THEN
                  Sleep(5*ClockFreq)
               END
            END
         END
      END
   UNTIL done
END GetCmd ;


PROCEDURE TooTired (p: CARDINAL) : BOOLEAN ;
VAR
   tired : BOOLEAN ;
BEGIN
   GetReadAccessToPlayerNo(p) ;
   tired := Tired(p) ;
   ReleaseReadAccessToPlayerNo(p) ;
   RETURN(tired)
END TooTired ;


PROCEDURE Tired (p: CARDINAL) : BOOLEAN ;
BEGIN
   WITH Player[p] DO
      RETURN (Fatigue< (((Weight * RequiredToAttack) DIV ManWeight)+10))
   END
END Tired ;


PROCEDURE Rest (p: CARDINAL) : BOOLEAN ;
BEGIN
   Sleep(5*ClockFreq) ;
   PutChar(' ') ;
   RETURN( TRUE )
END Rest ;


PROCEDURE Finish (p: CARDINAL) : BOOLEAN ;
VAR
   NeedToFinish: BOOLEAN ;
BEGIN
   GetReadAccessToAllPlayers ;
   IF Player[p].DeathType#living   (* If we have been killed *)
   THEN
      ReleaseReadAccessToAllPlayers ;
      GetAccessToScreenNo( p ) ;
      CurrentProcess^.PStream^.inchar := ManRead[p] ;
      Robot[p] := FALSE ;
      ReleaseAccessToScreenNo( p ) ;
      PutChar(' ') ;
      NeedToFinish := TRUE
   ELSE
      TestIfLastLivePlayer( NeedToFinish ) ;
      ReleaseReadAccessToAllPlayers ;
      IF NeedToFinish
      THEN
         PutStr('sOk I am The Conqueror') ;
         PutChar(cr) ; (* Exit Dungeon *)
         PutChar('|')
      END
   END ;
   RETURN( NeedToFinish )
END Finish ;


PROCEDURE Move (p: CARDINAL) : BOOLEAN ;
VAR
   enemy: CARDINAL ;
   moved: BOOLEAN ;
BEGIN
   GetEnemy(enemy) ;
   moved := NextToEnemy(enemy) ;
   RETURN( moved )
END Move ;


PROCEDURE GetEnemy (VAR enemy: CARDINAL) ;
VAR
   p,  r,
   p1, p2,
   w1, w2,
   n1, n2,
   r1, r2: CARDINAL ;
BEGIN
   p := PlayerNo() ;
   GetReadAccessToAllPlayers ;
   IF p=0
   THEN
      p1 := 1 ;
      WITH Player[1] DO
         w1 := Wounds ;
         r1 := RoomOfMan ;
         n1 := FarAway( Xman, Yman )
      END ;
      p2 := 2 ;
      WITH Player[2] DO
         w2 := Wounds ;
         r2 := RoomOfMan ;
         n2 := FarAway( Xman, Yman )
      END ;
   ELSIF p=1
   THEN
      p1 := 0 ;
      WITH Player[0] DO
         w1 := Wounds ;
         r1 := RoomOfMan ;
         n1 := FarAway( Xman, Yman )
      END ;
      p2 := 2 ;
      WITH Player[2] DO
         w2 := Wounds ;
         r2 := RoomOfMan ;
         n2 := FarAway( Xman, Yman )
      END
   ELSE
      p1 := 0 ;
      WITH Player[0] DO
         w1 := Wounds ;
         r1 := RoomOfMan ;
         n1 := FarAway( Xman, Yman )
      END ;
      p2 := 1 ;
      WITH Player[1] DO
         w2 := Wounds ;
         r2 := RoomOfMan ;
         n2 := FarAway( Xman, Yman )
      END
   END ;
   r := Player[p].RoomOfMan ;
   IF (r=r1) AND (r=r2)
   THEN
      IF n1<n2
      THEN
         enemy := p1
      ELSIF n2<n1
      THEN
         enemy := p2
      ELSE
         IF w1>w2
         THEN
            enemy := p1
         ELSE
            enemy := p2
         END
      END
   ELSIF r=r1
   THEN
      enemy := p1
   ELSIF r=r2
   THEN
      enemy := p2
   ELSE
      IF w1>w2
      THEN
         enemy := p1
      ELSE
         enemy := p2
      END
   END ;
   IF (Player[p1].DeathType=living) AND (Player[p2].DeathType=living)
   THEN
      IF Robot[p1]
      THEN
         enemy := p2
      ELSIF Robot[p2]
      THEN
         enemy := p1
      END
   END ;
   ReleaseReadAccessToAllPlayers ;
END GetEnemy ;


PROCEDURE FarAway (x, y: CARDINAL) : CARDINAL ;
VAR
   p: CARDINAL ;
BEGIN
   p := PlayerNo() ;
   WITH Player[p] DO
      IF x>Xman THEN x := x-Xman ELSE x := Xman-x END ;
      IF y>Yman THEN y := y-Yman ELSE y := Yman-y END
   END ;
   IF x>y
   THEN
      RETURN( x )
   ELSE
      RETURN( y )
   END
END FarAway ;


PROCEDURE NextToEnemy (enemy: CARDINAL) : BOOLEAN ;
VAR
   next,
   hit    : BOOLEAN ;
   x, y, i,
   p, cd  : CARDINAL ;
   xe, ye : CARDINAL ;
   r, re  : CARDINAL ;
BEGIN
   p := PlayerNo() ;
   GetReadAccessToAllPlayers ;
   WITH Player[p] DO
      r := RoomOfMan ;
      x := Xman ;
      y := Yman ;
      cd := Direction
   END ;
   WITH Player[enemy] DO
      re := RoomOfMan ;
      xe := Xman ;
      ye := Yman
   END ;
   ReleaseReadAccessToAllPlayers ;
   IF r#re
   THEN
      Sleep(4*ClockFreq) ;
      PutChar(' ') ;
      GetWriteAccessToAllPlayers ;
      re := Player[enemy].RoomOfMan ;
      IF (re=0) OR (Player[enemy].DeathType#living)
      THEN
         next := TRUE
      ELSE
         GetReadAccessToTreasure ;
         PositionInRoom( re, x, y, next ) ;
         ReleaseReadAccessToTreasure ;
         IF next  (* Now in room *)
         THEN
            EraseMan(p) ;
            WITH Player[p] DO
               RoomOfMan := re ;
               Xman := x ;
               Yman := y ;
               ScreenX := x-(x MOD Width) ;
               ScreenY := y-(y MOD Height) ;
            END ;
            ReleaseWriteAccessToAllPlayers ;
            InitialDisplay ;
            GetWriteAccessToAllPlayers ;
            DrawMan( p ) ;
         ELSE    (* Cannot get in *)
            PutStr('sHelp - cannot follow') ;
            PutChar(cr) ;
            next := TRUE
         END
      END ;
      ReleaseWriteAccessToAllPlayers
   ELSE
      (* Same room as enemy *)
      IF x>xe THEN xe := x-xe ELSE xe := xe-x END ;
      IF y>ye THEN ye := y-ye ELSE ye := ye-y END ;
      IF (xe>10) OR (ye>10)
      THEN
         Sleep(1*ClockFreq) ;
         next := Towards( p, enemy, x, y, 2, cd ) ;
         xe := x ; ye := y ;
         IncPosition( xe, ye, cd ) ;
         hit := PointOnPlayer( enemy, xe, ye )
      ELSE
         next := Towards( p, enemy, x, y, 5, cd ) ;
         xe := x ; ye := y ;
         IncPosition( xe, ye, cd ) ;
         hit := PointOnPlayer( enemy, xe, ye ) ;
         i := 0 ;
         WHILE (NOT hit) AND (i<2) DO
            IF Towards( p, enemy, x, y, 5, cd )
            THEN
               next := TRUE
            END ;
            xe := x ; ye := y ;
            IncPosition( xe, ye, cd ) ;
            hit := PointOnPlayer( enemy, xe, ye ) ;
            INC(i)
         END ;
         IF (NOT hit) AND (NOT Free(xe, ye, r)) AND (NOT next)
         THEN
            (* Try to go around abstacle *)
            x := xe ; y := ye ;
            IncPosition(x, y, (cd + 1) MOD 4) ;  (* right turn *)
            IF Free(x, y, r)
            THEN
               PutChar('l') ;   (* try left turn *)
               PutChar('1') ;
               PutChar('r') ;
               PutChar('1')
            ELSE
               PutChar('r') ;   (* right turn is ok *)
               PutChar('1') ;
               PutChar('l') ;
               PutChar('1')
            END ;
            next := TRUE
         END
      END
   END ;
   RETURN( next )
END NextToEnemy ;


PROCEDURE Towards (p, enemy: CARDINAL ;
                   VAR x, y: CARDINAL ;
                   n: CARDINAL ; VAR CurrentDir: CARDINAL) : BOOLEAN ;
VAR
   xe, ye, OldN,
   xt, yt      : CARDINAL ;
   yok, xok    : BOOLEAN ;
   moved       : BOOLEAN ;
BEGIN
   GetReadAccessToAllPlayers ;
   IF Player[enemy].DeathType=living
   THEN
      WITH Player[enemy] DO
         xe := Xman ;
         ye := Yman
      END ;
      xok := TRUE ; yok := TRUE ;
      OldN := n ;
      WHILE (n>0) AND (yok OR xok) DO
         IF xe<x
         THEN
            GoDirection( p, enemy, 1, x-xe, n, x, y, xok, CurrentDir )
         ELSIF xe>x
         THEN
            GoDirection( p, enemy, 3, xe-x, n, x, y, xok, CurrentDir )
         ELSE
            xok := FALSE
         END ;
         IF ye<y
         THEN
            GoDirection( p, enemy, 0, y-ye, n, x, y, yok, CurrentDir )
         ELSIF ye>y
         THEN
            GoDirection( p, enemy, 2, ye-y, n, x, y, yok, CurrentDir )
         ELSE
            yok := FALSE
         END
      END ;
      moved := (OldN#n)
   ELSE
      PutStr('sHe has died on me...') ;
      PutChar( cr ) ;
      moved := TRUE
   END ;
   ReleaseReadAccessToAllPlayers ;
   RETURN( moved )
END Towards ;


PROCEDURE GoDirection (p, enemy: CARDINAL ; dir, n: CARDINAL ;
                       VAR max, x, y: CARDINAL ;
                       VAR continue :BOOLEAN ; VAR CurrentDir: CARDINAL) ;
VAR
   OldN: CARDINAL ;
   r   : CARDINAL ;
   x1,y1: CARDINAL ;
BEGIN
   OldN := n ;
   r := Player[p].RoomOfMan ;
   continue := TRUE ;
   WHILE (max>0) AND (n>0) AND continue DO
      x1 := x ;
      y1 := y ;
      IncPosition( x1, y1, dir ) ;
      IF Free( x1, y1, r )
      THEN
         x := x1 ;
         y := y1 ;
         DEC(max) ;
         DEC(n)
      ELSE
         continue := FALSE
      END
   END ;
   IF dir#CurrentDir
   THEN
      dir := ((4+dir)-CurrentDir) MOD 4 ;
      IF dir=1
      THEN
         PutChar('l') ;  (* left turn *)
         CurrentDir := (1+CurrentDir) MOD 4
      ELSIF dir=3
      THEN
         PutChar('r') ;  (* right turn *)
         CurrentDir := (3+CurrentDir) MOD 4
      ELSIF dir=2
      THEN
         PutChar('v') ;  (* vault turn *)
         CurrentDir := (2+CurrentDir) MOD 4
      END
   END ;
   IF OldN>n
   THEN
      Sleep(1*ClockFreq) ;
(*
      WHILE OldN>n DO
         Sleep(1*ClockFreq) ;
         PutChar('1') ;
         DEC(OldN)
      END
*)
      (* PutChar( CHR(ORD('0')+OldN-n) ) *)
      PutChar('1') ;
   END
END GoDirection ;


PROCEDURE PointOnPlayer (p: CARDINAL ; x, y: CARDINAL) : BOOLEAN ;
BEGIN
   WITH Player[p] DO
      RETURN ((Xman=x) AND (Yman=y))
   END
END PointOnPlayer ;


PROCEDURE Free (x, y: CARDINAL ; r: CARDINAL) : BOOLEAN ;
VAR
   free: BOOLEAN ;
   i   : CARDINAL ;
BEGIN
   i := 0 ;
   free := TRUE ;
   WHILE free AND (i<=MaxNoOfPlayers) DO
      free := NOT PointOnPlayer( i, x, y ) ;
      INC(i)
   END ;
   IF free
   THEN
      PointOnWall( r, x, y, free ) ;
      free := NOT free ;
      IF free
      THEN
         GetReadAccessToTreasure ;
         PointOnTreasure( r, x, y, i, free ) ;
         ReleaseReadAccessToTreasure ;
         free := NOT free
      END
   END ;
   RETURN( free )
END Free ;


(*
   IsOnTreasure - returns true if the point x, y in room, Room,
                  is on treasure.
*)

PROCEDURE IsOnTreasure (Room: CARDINAL; x, y: CARDINAL) : BOOLEAN ;
VAR
   i: CARDINAL ;
   Hit: BOOLEAN ;
BEGIN
   PointOnTreasure( Room, x, y, i, Hit ) ;
   RETURN( Hit )
END IsOnTreasure ;


PROCEDURE Fight (p: CARDINAL) : BOOLEAN ;
VAR
   e    : CARDINAL ;
   x, y : CARDINAL ;
   ok,
   NotProtected : BOOLEAN ;
BEGIN
   GetEnemy( e ) ;
   GetReadAccessToAllPlayers ;
   WITH Player[p] DO
      x := Xman ;
      y := Yman ;
      NotProtected := NOT (MagicShield IN Player[e].TreasureOwn) ;
      IncPosition( x, y, Direction ) ;
      IF PointOnPlayer( e, x, y )
      THEN
         IF (NoOfMagic>0) AND
            (Fatigue> (Weight * RequiredToFireMagic) DIV ManWeight)
         THEN
            PutChar('m')
         ELSIF (NoOfNormal>0) AND
               (Fatigue> (Weight * RequiredToFireArrow) DIV ManWeight) AND
               NotProtected
         THEN
            PutChar('f')
         ELSE
            PutChar('a')
         END ;
         ok := TRUE
      ELSE
         ok := FALSE
      END
   END ;
   ReleaseReadAccessToAllPlayers ;
   RETURN( ok )
END Fight ;



PROCEDURE DodgeArrows (p: CARDINAL) : BOOLEAN ;
VAR
   x, y, pl, d,
   r           : CARDINAL ;
   hit         : BOOLEAN ;
   ad, ax, ay  : CARDINAL ;
BEGIN
   GetReadAccessToAllPlayers ;
   WITH Player[p] DO
      x := Xman ;
      y := Yman ;
      d := Direction ;
      r := RoomOfMan
   END ;
   hit := FALSE ;
   pl := 0 ;
   WHILE (pl<=MaxNoOfPlayers) AND (NOT hit) DO
      IF p#pl
      THEN
         WITH Player[pl] DO
            IF NOT Awaited( OkToStartMagic )
            THEN
               UpdateNearest( x, y, ArrowXMagic, ArrowYMagic, ArrowDirMagic,
                              ax, ay, ad, hit )
            END ;
            IF (NOT Awaited( OkToStartNormal )) AND (NOT hit)
            THEN
               UpdateNearest( x, y, ArrowXNormal, ArrowYNormal, ArrowDirNormal,
                              ax, ay, ad, hit )
            END
         END
      END ;
      INC( pl )
   END ;
   IF hit
   THEN
      Avoid( p, x, y, d, ax, ay, ad ) ;
      ReleaseReadAccessToAllPlayers ;
   ELSE
      ReleaseReadAccessToAllPlayers ;
   END ;
   RETURN( hit )
END DodgeArrows ;


PROCEDURE Avoid (p, x, y, d, ax, ay, ad: CARDINAL) ;
VAR
   z, td, r,
   tx, ty: CARDINAL ;
BEGIN
   r := Player[p].RoomOfMan ;
   (* Our man wants to face arrow and then turn either way *)
   (* so:                                                  *)
   (*     (ad+2) MOD 4 = d + z  operator                   *)
   (* therefore:                                           *)
   (*     (ad+2-d) MOD 4 = z                               *)

   z := (ad+6-d) MOD 4 ;

   (* try dodging by turning left.                         *)

   td := (z+1) MOD 4 ;
   tx := x ;
   ty := y ;
   IncPosition( tx, ty, td ) ;
   IF Free(tx, ty, r)
   THEN
      IF td#0 THEN PutChar( GetDirChar(td) ) END ;
      PutChar('1')
   ELSE
      td := (z+3) MOD 4 ;  (* add Right turn *)
      tx := x ;
      ty := y ;
      IncPosition( tx, ty, td ) ;
      IF Free(tx, ty, r)
      THEN
         IF td#0 THEN PutChar( GetDirChar(td) ) END ;
         PutChar('1')
      ELSE
         WriteString('trying to jump it') ;
         (* face arrow and try to jump it *)
         IF z#0 THEN PutChar( GetDirChar(z) ) END ;
         PutChar('6')
      END
   END
END Avoid ;


PROCEDURE GetDirChar (d: CARDINAL) : CHAR ;
VAR
   ch: CHAR ;
BEGIN
   IF d=1
   THEN
      ch := 'l'
   ELSIF d=3
   THEN
      ch := 'r'
   ELSIF d=2
   THEN
      ch := 'v'
   END ;
   RETURN( ch )
END GetDirChar ;


PROCEDURE UpdateNearest( x, y,
                         ArrowX, ArrowY, ArrowDir: CARDINAL ;
                         VAR ax, ay, ad: CARDINAL ;
                         VAR hit: BOOLEAN) ;
BEGIN
   IF (ArrowDir=0) AND (ArrowY>y)
   THEN
      hit := (ArrowX=x)
   ELSIF (ArrowDir=2) AND (ArrowY<y)
   THEN
      hit := (ArrowX=x)
   ELSIF (ArrowDir=1) AND (ArrowX>x)
   THEN
      hit := (ArrowY=y)
   ELSIF (ArrowX<x)
   THEN
      hit := (ArrowY=y)
   END ;
   IF hit
   THEN
      ax := ArrowX ;
      ay := ArrowY ;
      ad := ArrowDir
   END
END UpdateNearest ;


PROCEDURE PutStr (a: ARRAY OF CHAR) ;
VAR
   i, high: CARDINAL ;
BEGIN
   high := StrLen(a) ;
   i := 0 ;
   WHILE i<high DO
      PutChar(a[i]) ;
      INC(i)
   END
END PutStr ;


PROCEDURE PutChar (ch: CHAR) ;
VAR
   p: CARDINAL ;
BEGIN
   p := PlayerNo() ;
   WITH ManBuffer[p] DO
      INC(no) ;
      buf[in] := ch ;
      in := (in+1) MOD MaxBufferSize
   END
END PutChar ;


PROCEDURE GetChar (VAR ch: CHAR) ;
VAR
   p: CARDINAL ;
BEGIN
   p := PlayerNo() ;
   WITH ManBuffer[p] DO
      DEC(no) ;
      ch := buf[out] ;
      out := (out+1) MOD MaxBufferSize
   END
END GetChar ;


PROCEDURE Empty () : BOOLEAN ;
BEGIN
   RETURN (ManBuffer[PlayerNo()].no=0)
END Empty ;


PROCEDURE InitBuffer ;
BEGIN
   WITH ManBuffer[PlayerNo()] DO
      out := 0 ;
      in := 0 ;
      no := 0
   END
END InitBuffer ;



BEGIN
   Robot[0] := FALSE ;
   Robot[1] := FALSE ;
   Robot[2] := FALSE
END AdvAuto.
(*
 * Local variables:
 *  compile-command: "make"
 * End:
 *)
