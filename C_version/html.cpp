#include "html.hpp"

String get_website_head() {
  String r =
    "<head>"
    "<style>html { font-family: Charter;}"
    "</style></head><main>"
    "<header> <meta http-equiv=\\refresh\\content=\\10\\></header>"
    "<p></p>"
    "<hr size=20 color=#b90f22> <hr size=4 color=#000000>"
    "<p></p>"
    "<CENTER> <img src='https://www.ptw.tu-darmstadt.de/media/fachgebietptw/grafikenundfotos/logos_2/PTW-Logo.png' width=140 height=92> </center>"
    "<center><h1>Smart Office Station</h1></center>"
    "<hr size=4 color=#000000>"
    "<p></p>"
    "<center><p><h2> Sensoren:</h2> </p></center>";
  return r;
}

String get_website_tail(){return "</main>";}

String get_window_head(String svg_image_link) {
	return "<center>"
	"<table style=\\height: 10px; width: 15%; bordercolor=#ffffff; border-collapse: collapse; border-style: hidden;\\ border=\\1\\>"
	"<tbody>"
	"<tr style=\\height: 10px;\\>"
	"<td style=\\width: 50%; height: 10px;\\>"
	"<center>"
	"<svg xmlns=\\http://www.w3.org/2000/svg\\ width=\\50\\ height=\\50\\ fill=\\currentColor\\ class=\\bi bi-cup-straw\\ viewBox=\\0 0 16 16\\>"
	"</svg>"
	"</center>"
	"</td>"
	"<td style=\\width: 50%; text-align: left; height: 10px;\\>"
	"<center>";
}

String get_window_tail() {
	return
		"</center>"
		"</td>"
		"</tr>"
		"</tbody>"
		"</table>"
		"</center>"
		"<p></p>"
		"<hr size=4 color=#000000>"
		"<p></p>  ";
	}

String get_window(String svg_image_link, String content) {
	return get_window_head(svg_image_link) + content + get_window_tail();
}
