IMPLEMENTATION MODULE GraphicTitle ;


FROM SVGA IMPORT GraphicsMode, vga_setmode, vga_getxdim, vga_getydim ;
FROM GraphicText IMPORT LoadFont, WriteString, Write, SetPosition, WidthString ;
FROM TTIO IMPORT Read ;
IMPORT StrIO ;


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
   Title - generate a pretty title for Morloc.
*)

PROCEDURE Title ;
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
END Title ;


END GraphicTitle.
