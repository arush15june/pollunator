(window.webpackJsonp=window.webpackJsonp||[]).push([[0],{29:function(t,e,n){},37:function(t,e,n){t.exports=n(79)},43:function(t,e,n){},79:function(t,e,n){"use strict";n.r(e);var a=n(0),r=n.n(a),i=n(21),s=n.n(i),o=(n(43),n(9)),c=n(10),u=n(12),l=n(11),h=n(13),p=n(2),f=n.n(p),d=n(8),v=n(35),m=n.n(v),g=n(22),w=n.n(g),b=n(17),S=n.n(b),k=n(16),y=n.n(k),j=function(t){function e(){return Object(o.a)(this,e),Object(u.a)(this,Object(l.a)(e).apply(this,arguments))}return Object(h.a)(e,t),Object(c.a)(e,[{key:"stationsRenderList",value:function(){return this.props.stationList.map(function(t){return r.a.createElement("option",{value:t.station_id},t.station_name)})}},{key:"render",value:function(){var t=this.stationsRenderList();return r.a.createElement(r.a.Fragment,null,r.a.createElement(y.a,{onChange:this.props.selectHandler},r.a.createElement(y.a.Group,{controlId:"formStationsList"},r.a.createElement(y.a.Label,null,"Stations"),r.a.createElement(y.a.Control,{controlId:"station",as:"select"},t))))}}]),e}(a.Component),O=n(14),E=n.n(O);var x=function(t){function e(){return Object(o.a)(this,e),Object(u.a)(this,Object(l.a)(e).apply(this,arguments))}return Object(h.a)(e,t),Object(c.a)(e,[{key:"parameterList",value:function(){return this.props.stationData.parameters.parameters.map(function(t){return r.a.createElement("p",null,t.name,": ",r.a.createElement("span",{className:"font-weight-bold"},t.value)," ",t.date)})}},{key:"render",value:function(){var t,e=this.props.stationData;return r.a.createElement(r.a.Fragment,null,(t=e,0!==Object.keys(t).length?r.a.createElement(E.a,null,r.a.createElement(E.a.Header,null,e.station_name),r.a.createElement(E.a.Body,null,r.a.createElement(E.a.Title,null,e.status),r.a.createElement(E.a.Text,null,"Latitude: ",e.latitude," Longitude: ",e.longitude," Timestamp: ",e.parameters.date),r.a.createElement(E.a.Text,null,this.parameterList()))):r.a.createElement(r.a.Fragment,null)))}}]),e}(a.Component),L=function(){function t(e,n){Object(o.a)(this,t),this.heapSize=-1,this.heap=Array(e).fill(-1),this.getValue=n}return Object(c.a)(t,[{key:"insert",value:function(t){if(this.heapSize+1===this.heap.length)throw"Overflow Size";this.heap[this.heapSize+1]=t,this.heapSize=this.heapSize+1,this.siftUp(this.heapSize)}},{key:"swap",value:function(t,e){var n=[this.heap[e],this.heap[t]];this.heap[t]=n[0],this.heap[e]=n[1]}},{key:"siftDown",value:function(t){var e=t,n=this.heap.length,a=2*t+1;a<=n-1&&this.getValue(this.heap[a])<this.getValue(this.heap[e])&&(e=a);var r=2*t+2;r<=n-1&&this.getValue(this.heap[a])<this.getValue(this.heap[e])&&(e=r),e!=t&&(this.swap(t,e),this.siftDown(e))}},{key:"siftUp",value:function(t){for(var e=Math.ceil((t-1)/2);t>0&&this.getValue(this.heap[e])>this.getValue(this.heap[t]);)this.swap(t,e),t=e,e=Math.ceil((t-1)/2)}},{key:"extractMin",value:function(){var t=this.heap[0];return this.heap[0]=this.heap[this.heapSize],this.heapSize=this.heapSize-1,this.siftDown(0),t}}]),t}(),C="".concat("").concat("/api/stations"),D=function(t){function e(t){var n;return Object(o.a)(this,e),(n=Object(u.a)(this,Object(l.a)(e).call(this,t))).selectChangeHandler=function(){var t=Object(d.a)(f.a.mark(function t(e){var a,r;return f.a.wrap(function(t){for(;;)switch(t.prev=t.next){case 0:return n.setState({selectedStation:{}}),a=e.target.value,t.next=4,n.fetchStationData(a);case 4:r=t.sent,n.setState({selectedStation:r});case 6:case"end":return t.stop()}},t)}));return function(e){return t.apply(this,arguments)}}(),n.state={stationList:[],stationDistanceList:[],coords:{},selectedStation:{}},n}return Object(h.a)(e,t),Object(c.a)(e,[{key:"fetchStationData",value:function(){var t=Object(d.a)(f.a.mark(function t(e){var n,a,r;return f.a.wrap(function(t){for(;;)switch(t.prev=t.next){case 0:return n="".concat(C,"/").concat(e),t.next=3,fetch(n);case 3:return a=t.sent,t.next=6,a.json();case 6:return r=t.sent,t.abrupt("return",r);case 8:case"end":return t.stop()}},t)}));return function(e){return t.apply(this,arguments)}}()},{key:"getStationFromStationId",value:function(t){var e=this.state.stationList.filter(function(e){return e.station_id===t})[0];return void 0===e?{}:e}},{key:"setUserCoordinates",value:function(){var t=Object(d.a)(f.a.mark(function t(){var e,n,a=this;return f.a.wrap(function(t){for(;;)switch(t.prev=t.next){case 0:e=navigator.geolocation,n=function(t){a.setState({coords:t})},e&&e.getCurrentPosition(n);case 3:case"end":return t.stop()}},t)}));return function(){return t.apply(this,arguments)}}()},{key:"euclideanDistance",value:function(t,e,n,a){return Math.sqrt(Math.pow(t-n,2)+Math.pow(e-a,2))}},{key:"setStationOnEuclideanDistance",value:function(){var t=Object(d.a)(f.a.mark(function t(){var e,n,a,r,i,s,o,c;return f.a.wrap(function(t){for(;;)switch(t.prev=t.next){case 0:if(0===this.state.coords.length||0===this.state.stationList.length){t.next=10;break}for(e=this.state.coords.coords.latitude,n=this.state.coords.coords.longitude,a=new L(this.state.stationList.length,function(t){return t.distance}),r=0;r<this.state.stationList.length;r++)i=this.state.stationList[r],s=i.latitude,o=i.longitude,c=this.euclideanDistance(e,n,s,o),i.distance=c,a.insert(i);return a.heap[0].station_name+=" [Nearest Geolocated Station]",this.setState({selectedStation:{}}),t.next=9,this.setSelectedStationFromStation(a.heap[0]);case 9:this.setState({stationList:a.heap});case 10:case"end":return t.stop()}},t,this)}));return function(){return t.apply(this,arguments)}}()},{key:"fetchStations",value:function(){var t=Object(d.a)(f.a.mark(function t(){var e,n;return f.a.wrap(function(t){for(;;)switch(t.prev=t.next){case 0:return t.next=2,fetch(C);case 2:return e=t.sent,t.next=5,e.json();case 5:n=t.sent,this.setState({stationList:n});case 7:case"end":return t.stop()}},t,this)}));return function(){return t.apply(this,arguments)}}()},{key:"setSelectedStationFromStation",value:function(){var t=Object(d.a)(f.a.mark(function t(e){var n;return f.a.wrap(function(t){for(;;)switch(t.prev=t.next){case 0:return t.next=2,this.fetchStationData(e.station_id);case 2:n=t.sent,console.log(n),this.setState({selectedStation:n});case 5:case"end":return t.stop()}},t,this)}));return function(e){return t.apply(this,arguments)}}()},{key:"setSelectedStationFromIndex",value:function(){var t=Object(d.a)(f.a.mark(function t(e){var n;return f.a.wrap(function(t){for(;;)switch(t.prev=t.next){case 0:return n=this.state.stationList[e],t.next=3,this.setSelectedStationFromStation(n);case 3:case"end":return t.stop()}},t,this)}));return function(e){return t.apply(this,arguments)}}()},{key:"componentDidMount",value:function(){var t=Object(d.a)(f.a.mark(function t(){return f.a.wrap(function(t){for(;;)switch(t.prev=t.next){case 0:return t.next=2,this.setUserCoordinates();case 2:return t.next=4,this.fetchStations();case 4:return t.next=6,this.setSelectedStationFromIndex(0);case 6:return t.next=8,this.setStationOnEuclideanDistance();case 8:case"end":return t.stop()}},t,this)}));return function(){return t.apply(this,arguments)}}()},{key:"render",value:function(){return r.a.createElement(r.a.Fragment,null,r.a.createElement(m.a,null,r.a.createElement(w.a,null,r.a.createElement(S.a,null,r.a.createElement(j,{stationList:this.state.stationList,selectHandler:this.selectChangeHandler}))),r.a.createElement(w.a,null,r.a.createElement(S.a,null,r.a.createElement(x,{stationData:this.state.selectedStation})))))}}]),e}(a.Component),F=n(23),z=n.n(F),M=(n(29),function(t){function e(){return Object(o.a)(this,e),Object(u.a)(this,Object(l.a)(e).apply(this,arguments))}return Object(h.a)(e,t),Object(c.a)(e,[{key:"render",value:function(){return r.a.createElement(r.a.Fragment,null,r.a.createElement(z.a,{bg:"dark",variant:"dark"},r.a.createElement(z.a.Brand,null,"Pollunator")))}}]),e}(a.Component)),U=function(t){function e(){return Object(o.a)(this,e),Object(u.a)(this,Object(l.a)(e).apply(this,arguments))}return Object(h.a)(e,t),Object(c.a)(e,[{key:"render",value:function(){return r.a.createElement(r.a.Fragment,null,r.a.createElement(M,null),r.a.createElement(D,null))}}]),e}(a.Component);n(36),"".concat("localhost:5000","/publickey");var V=Boolean("localhost"===window.location.hostname||"[::1]"===window.location.hostname||window.location.hostname.match(/^127(?:\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}$/));function W(t,e){navigator.serviceWorker.register(t).then(function(t){t.onupdatefound=function(){var n=t.installing;null!=n&&(n.onstatechange=function(){"installed"===n.state&&(navigator.serviceWorker.controller?(console.log("New content is available and will be used when all tabs for this page are closed. See https://bit.ly/CRA-PWA."),e&&e.onUpdate&&e.onUpdate(t)):(console.log("Content is cached for offline use."),e&&e.onSuccess&&e.onSuccess(t)))})}}).catch(function(t){console.error("Error during service worker registration:",t)})}s.a.render(r.a.createElement(U,null),document.getElementById("root")),function(t){if("serviceWorker"in navigator){if(new URL("",window.location.href).origin!==window.location.origin)return;window.addEventListener("load",function(){var e="".concat("","/service-worker.js");V?(function(t,e){fetch(t).then(function(n){var a=n.headers.get("content-type");404===n.status||null!=a&&-1===a.indexOf("javascript")?navigator.serviceWorker.ready.then(function(t){t.unregister().then(function(){window.location.reload()})}):W(t,e)}).catch(function(){console.log("No internet connection found. App is running in offline mode.")})}(e,t),navigator.serviceWorker.ready.then(function(){console.log("This web app is being served cache-first by a service worker. To learn more, visit https://bit.ly/CRA-PWA")})):W(e,t)})}}()}},[[37,1,2]]]);
//# sourceMappingURL=main.c7398daf.chunk.js.map