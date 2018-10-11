IMPLEMENTATION MODULE Title ;


FROM SVGA IMPORT GraphicsMode, vga_setmode, vga_getxdim, vga_getydim ;
FROM GraphicText IMPORT LoadFont, WriteString, Write, SetPosition, WidthString ;
FROM TTIO IMPORT Read ;
IMPORT SerIOA ;
IMPORT StrIO ;
IMPORT StdIO ;
FROM Capability IMPORT TerminalCapability, InitCapability,
                       Move, Clear, Home, Reverse, Normal ;


(*
   CentreString - centres string, a, on the graphics screen.
*)

PROCEDURE CentreString (a: ARRAY OF CHAR; y: CARDINAL) ;
VAR
   Width: CARDINAL ;
BEGIN
   SetPosition((vga_getxdim()-WidthString(a)) DIV 2, y) ;
   WriteString(a)
END CentreString ;


(*
   GraphicTitle - generate a pretty title for Morloc.
*)

PROCEDURE GraphicTitle ;
VAR
   ch: CHAR ;
BEGIN
   StrIO.WriteString('The revenge of morloc...') ;
   Read(ch) ;
   IF LoadFont('alpha/small')
   THEN
      Read(ch) ;
      vga_setmode(G320x200x16) ;
      CentreString('Welcome to Morloc Tower...', vga_getydim() DIV 9) ;
      Read(ch) ;
      vga_setmode(G640x480x16) ;
      CentreString("Morloc Tower is written in Modula 2 generating 386 486 code", vga_getydim() DIV 9) ;
      CentreString('and it employs a preemptive realtime operating system', 2 * vga_getydim() DIV 9) ;
   ELSE
      StrIO.WriteString('The revenge of morloc...')
   END ;
   StrIO.WriteString('Morloc finished') ;
END GraphicTitle ;


(*
   BasicTitle - generate a pretty title for Morloc.
*)

PROCEDURE BasicTitle ;
VAR
   ch: CHAR ;
   t : TerminalCapability ;
BEGIN
   StdIO.PushOutput(SerIOA.Write) ;
   t := InitCapability('console') ;
   IF t=NIL
   THEN
      StrIO.WriteString('dont know about terminal gigi') ;
      HALT ;
   END ;
   Clear(t) ;
   Home(t) ;
   Move(t, 10, 8) ;
   Reverse(t) ;
   StrIO.WriteString('The revenge of morloc...') ;
   Normal(t) ;
   Move(t, 1, 1)
END BasicTitle ;


END Title.
