# Network quality test framework

## ICMPv4 request/response test

_ping.py_ is running continuous test against _IP_ and collects:
  * packet loss rate
  * minimum response time
  * maximum response time
  * average response time
  
Results are peridocally displayed on the screen and written to figures in _Results_ folder. 

For instance, the following figures demonstrate network quality issues during first phase of monitoring:

![Sample loss rate](/Docs/f_loss.png "Sample loss rate")
![Sample response time](/Docs/f_minmaxavf "Sample min/max/avg response time")