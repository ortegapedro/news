

      var tamNube;



      $(document).on('input', '#slider', function() {

        $('#slider_value').html( $(this).val() );
        tamNube = $(this).val()
        console.log(tamNube)

       });

      function mostrarNube(categoria){

           document.getElementById("cloud").innerHTML="";
            $.getJSON('/cloud/'+categoria, function(obj){

            var words = obj;
            console.log(categoria)
            var lista = $("#cloud").jQCloud(words);
            console.log(lista.typeof)
      });
      }

      function mostrarNubeQuery(){

           document.getElementById("cloud").innerHTML="";
            $.getJSON('/cloudQuery', function(obj){

            var words = obj;
            console.log(obj)
            $("#cloud").jQCloud(words);

      });
      }



      ////////////////////////////////////////////////////////////


      function news(contenido,coords){
      //console.log(contenido+"___"+coords);

        var iconFeature2 = new ol.Feature({
        geometry: new ol.geom.Point(coords),
        name: contenido
      });
        return iconFeature2;
      }


      //var coords=[[-6499005.43073,-4110153.01627],[-11036347.9006,2206241.27793],[-5780295.7289,-1601191.81344],[1163458.55233,6650655.04117],[-11035458.2353,2205935.2699]];


      function setContenidoPopUp(listaContenidos,listaCordenadas){
      var listaDeIconos =[];

        for (i = 0; i < listaContenidos.length; i++) {

        var contenido=listaContenidos[i];
        var coords=listaCordenadas[i];
        //console.log(contenido)
        iconFeature2=news(contenido,coords)
        iconFeature2.setStyle(iconStyle);
        listaDeIconos.push(iconFeature2);
       }

        var iconStyle = new ol.style.Style({
        image: new ol.style.Icon(/** @type {olx.style.IconOptions} */ ({
          anchor: [0.5, 46],
          anchorXUnits: 'fraction',
          anchorYUnits: 'pixels',
          src: 'http://openlayers.org/en/v3.18.2/examples/data/icon.png'
        }))
      });

       for (i = 0; i < listaDeIconos.length; i++) {
          listaDeIconos[i].setStyle(iconStyle);
      }


      console.log(listaDeIconos);

      var vectorSource = new ol.source.Vector({
        features: listaDeIconos
      });

       var vectorLayer = new ol.layer.Vector({
        source: vectorSource
      });
        return vectorLayer;
      }

     //console.log(fruits)


      function createMap(vectorLayer){
        //layer de mapa
          var rasterLayer = new ol.layer.Tile({
             source: new ol.source.OSM()
          });

           console.log("raster layer: ",rasterLayer);
           console.log("vectro layer:",vectorLayer);

          var map = new ol.Map({
            layers: [rasterLayer, vectorLayer],
            target: document.getElementById('map'),
            view: new ol.View({
              center: [0, 0],
              zoom: 3
            })
          });

           return map;
       }

       var map;
       var element = document.getElementById('popup');
      function getNews(query){

            document.getElementById("mytable").innerHTML="";
            document.getElementById("mostrar").innerHTML="";
            document.getElementById("cloud").innerHTML="";
            document.getElementById("chart").innerHTML="";
            document.getElementById("cardT1").innerHTML="";
            document.getElementById("nNoticias").innerHTML="";
            document.getElementById("nTopicos").innerHTML="";
            document.getElementById("map").innerHTML="";



            //networkWords()
              var radios = document.getElementsByName('category');
              var categoria="";
                for (var i = 0, length = radios.length; i < length; i++) {
                    if (radios[i].checked) {
                        // do whatever you want with the checked radio
                        //alert(radios[i].value);

                        categoria=radios[i].value;
                        console.log(categoria)
                        // only one radio can be logically checked, don't check the rest
                        break;
                    }
                }
              fecha=getDates()
              dataToQuery=fecha[0]+"||"+fecha[1]+"||"+categoria+"||"+query
              console.log(dataToQuery)
             $.getJSON('/query/'+dataToQuery, function(obj){

                    var words = obj[0]["cloud"];

                    $("#cloud").jQCloud(words);
                    //

                   //var tbl=$("<table><tr><td>   Fecha</td><td>   Titulo</td><td>   Descripcion</td></tr>").attr("id","mytable");
                   //var tbl=$('<div class="card-deck-wrapper">');
                   //$("#mostrarNews").append(tbl);
                   var data=obj[0]["news"]
                    //Documentos recuperados
                    console.log("noticias: ",data.length)

                   var tbl=$('');
                   var listaContenidos=[]
                   var listaCordenadas=[]
                   for (var j=1; j<2;j++){
                       for(var i=0;i<data.length;i++)
                          {

                               var src=data[i]["linkImage"];
                               var card_title=data[i]["Titulo"];
                               var card_text=data[i]["Descripcion"];
                               var linkBoton=data[i]["link"];
                               var Fecha=data[i]["Fecha"];
                               var Topic=data[i]["topic"];
                               var locations=data[i]["location"];
                               //console.log("Locations: "+locations[0]);

                               var contenido='<p class="card-text"><small class="text-muted">Topic '+Topic+'</small> </p><div class="card-deck"><div class="card"><img class="card-img-top" src="'+src+'" alt="Card image cap" WIDTH=319px HEIGHT=180px BORDER=2 ALT="Obra de K. Haring" ><div class="card-block">    <h4 class="card-title">'+card_title+'</h4><p class="card-text">'+card_text+'</p><p class="card-text"><small class="text-muted">"'+Fecha+'"</small> </p><a href="'+linkBoton+'" class="btn btn-primary" target="_blank">Enlace</a></div></div><br>';
                               //se tiene que pasar una lista c
                               var coord = locations[0].split(",");
                               //console.log(coord);
                               var cordenadas=[parseFloat(coord[0]),parseFloat(coord[1])];
                                listaContenidos.push(card_title);
                                listaCordenadas.push(cordenadas);

                                var tbl=$(contenido);
                               //$("#cardT"+j.toString()).append(tbl);
                               $("#cardT1").append(tbl);
                          }
                     //$("#mostrarNews").append('</div>');
                    }

                    ///////////////////////////////////////////
                    //console.log("primer html text: "+listaContenidos[0]);
                    //console.log("location: "+listaCordenadas[0]);
                    console.log(listaCordenadas);
                    console.log(listaContenidos);
                    var vectorLayer = setContenidoPopUp(listaContenidos,listaCordenadas);
                    console.log(vectorLayer);
                    map = createMap(vectorLayer);
                    console.log("map: ",map);



                    console.log("element: ",element);
                      var popup = new ol.Overlay({
                        element: element,
                        positioning: 'bottom-center',
                        stopEvent: false,
                        offset: [0, -50]
                      });
                      map.addOverlay(popup);

                      // display popup on click
                      map.on('click', function(evt) {
                      console.log("click in map");
                        var feature = map.forEachFeatureAtPixel(evt.pixel,
                            function(feature) {
                              return feature;
                            });
                        if (feature) {
                          var coordinates = feature.getGeometry().getCoordinates();
                          console.log(feature.get('name'),"cordinates: ",coordinates);
                          popup.setPosition(coordinates);

                          $(element).popover({
                            'placement': 'top',
                            'html': true,
                            'content': feature.get('name')
                          });
                          $(element).popover('show');
                          console.log("element: ", element);
                        } else {

                          $(element).popover('destroy');
                        }
                      });

                      // change mouse cursor when over marker
                      map.on('pointermove', function(e) {
                        if (e.dragging) {
                          $(element).popover('destroy');
                          return;
                        }
                        var pixel = map.getEventPixel(e.originalEvent);
                        var hit = map.hasFeatureAtPixel(pixel);
                        map.getTarget().style.cursor = hit ? 'pointer' : '';
                      });


                /////////////////////////////////////////////

                    var jsonGraph = obj[0]["Groups"]
                    console.log("bulding the graph");



                    var numeroDeTopicos=obj[0]["jsonGraph"];
                    console.log(numeroDeTopicos["Groups"]);

                    $("#nNoticias").append('<h2><span class="label label-success"> Noticias: '+data.length+'</span></h1>');
                    $("#nTopicos").append('<h2><span class="label label-success">Topicos: '+numeroDeTopicos["Groups"]+'</span></h1>');


                    //networkWords(obj[0]["jsonGraph"]);

                   //console.log(networkWords(obj[0]["jsonGraph"]));
                   //console.log(obj[0]["cloud"]);



      });
      }





     /////////////////////////////////////////////////////////////
      function getQuery(){

          //var jobValue = document.getElementById('txtJob').value

          var jobValue = document.getElementById('txtJob').value

          getNews(jobValue)
          //mostrarNubeQuery()
          console.log(jobValue)
      }

      var myCalendar;

      function getNewsByDate(date){

            document.getElementById("mytable").innerHTML="";
            document.getElementById("mostrar").innerHTML="";
            document.getElementById("cloud").innerHTML="";

             $.getJSON('/today/'+date, function(obj){

                    var words = obj[0]["cloud"];
                    $("#cloud").jQCloud(words);

                    var tbl=$("<table><tr><td>   Fecha</td><td>   Titulo</td><td>   Descripcion</td></tr>").attr("id","mytable");
                   $("#mostrar").append(tbl);
                   var data=obj[0]["news"]
                   for(var i=0;i<data.length;i++)
                      {
                        var tr="<tr>";
                        var td1="<td>"+data[i]["Fecha"]+"</td>";
                        var td2="<td>"+data[i]["Titulo"]+"</td>";
                        var td3="<td>"+data[i]["Descripcion"]+"</td></tr>";

                       $("#mytable").append(tr+td1+td2+td3);

                      }
                   console.log(obj[0]["news"]);
                   console.log(obj[0]["cloud"]);

      });
      }

      function mostrarNubeInicio(fecha){

           document.getElementById("cloud").innerHTML="";
            $.getJSON('/cloudInicio/'+fecha, function(obj){

            var words = obj;
            //console.log(fecha)
            var lista = $("#cloud").jQCloud(words);

      });
      }

	  function doOnLoad() {

            //mostrarCards()
            getDates()

			//getNewsByDate(date_to)
			//networkWords()
            //mostrarCards()
		}

        function getDates(){
            myCalendar = new dhtmlXCalendarObject(["date_from","date_to"]);
			myCalendar.setDate("2016-09-21");
			myCalendar.hideTime();

			// init values
			date_from=byId("date_from").value = "2016-09-21";

			var f = new Date();
			date_to = f.getFullYear() + "-" + (f.getMonth() +1) + "-" + f.getDate()
			byId("date_to").value = date_to;

			console.log(date_from)
			console.log(date_to)
			var dates=[date_from,date_to]
			return dates
        }
		function setSens(id, k) {
			// update range
			if (k == "min") {
				myCalendar.setSensitiveRange(byId(id).value, null);
			} else {
				myCalendar.setSensitiveRange(null, byId(id).value);
			}
		}
		function byId(id) {
			return document.getElementById(id);
		}

      $(function(){
            $('#t').keypress(function(e){
                var txt = String.fromCharCode(e.which);
                console.log(txt + ' : ' + e.which);
                if(!txt.match(/[A-Za-z0-9+#.]/))
                {
                    return false;
                }
            });
        });



      /*Grafo  de palabras
      */

(function() {
    /* test data in data/fm.json */
    /*
       (a)---------(b)  (c)---------(d)
           |  |  |           |  |
    (e)---(f)(g)(h)---------(i)(j)---(k)
        |                          |
       (l)------------------------(m)
                     |
                    (n)
    */

    // add a method conditionaly
    if (!('xpush' in Array.prototype)) {
        // push value to array only if not already present
        Array.prototype.xpush = function(value) {
            if (this.indexOf(value) === -1) {
                this.push(value);
            }
            return this;
        };
    };

    d3.graphSub = function() {

        var config = {
            width: 1000,
            height: 500,
            hops: 2
        };

        function chart(selection) {
            selection.each(function(d, i) {

                // DOM to which to attach the vizualization
                var current_selection = this;

                var model = {};

                var controller = {

                    init: function() {
                        model.graph = d;
                        model.force = d3.layout.force();
                        model.force2 = d3.layout.force();
                        model.subNetNodes = model.force.nodes();
                        model.subNetLinks = model.force.links();
                        model.linkStrings = [];
                        model.labelAnchors = model.force2.nodes();
                        model.labelAnchorLinks = model.force2.links();

                        // setup search-box data
                        model.nodeNames = [];
                        for (var i = 0; i < model.graph.nodes.length; i++) {
                            model.nodeNames.push({
                                'label': model.graph.nodes[i].name,
                                'value': i + ''
                            });
                        };

                        view.init();

                        this.getSubnet(0, 1)
                        this.click(model.subNetNodes[0]);
                    },

                    graphNodes: function() {
                        return model.graph.nodes;
                    },

                    graphLinks: function() {
                        return model.graph.links;
                    },

                    // add link to the layout
                    addLink: function(source, target, value) {
                        var link = {
                            "source": this.findNode(source),
                            "target": this.findNode(target),
                            "value": value
                        };
                        model.subNetLinks.push(link);
                    },

                    // look for the node in the d3 layout
                    findNode: function(name) {
                        for (var i in model.graph.nodes) {
                            if (model.graph.nodes[i]["name"] === name) return model.graph.nodes[i];
                        };
                    },

                    // remove all links from the layout
                    removeAllLinks: function(linkArray) {
                        linkArray.splice(0, linkArray.length);
                    },

                    // remove all node from the layout
                    removeAllNodes: function(nodeArray) {
                        nodeArray.splice(0, nodeArray.length);
                    },

                    findNodeIndex: function(name, nodes) {
                        for (var i = 0; i < nodes.length; i++) {
                            if (nodes[i].name == name) {
                                return i;
                            }
                        };
                    },

                    createAnchors: function() {
                        for (var i = 0; i < model.subNetNodes.length; i++) {
                            // one node is anchor to the force1 node
                            var n = {
                                label: model.subNetNodes[i]
                            };

                            model.labelAnchors.push({
                                node: n,
                                type: "tail"
                            });
                            model.labelAnchors.push({
                                node: n,
                                type: "head"
                            });
                        };
                    },

                    createAnchorLinks: function() {
                        for (var i = 0; i < model.subNetNodes.length; i++) {
                            // nodes are connected in pairs
                            model.labelAnchorLinks.push({
                                source: i * 2,
                                target: i * 2 + 1,
                                weight: 1
                            });
                        };
                    },

                    getSubnet: function(currentIndex, hops) {
                        // links stored as JSON objects, easy to compare
                        // operates on the data loaded from the JSON
                        var n = model.graph.nodes[currentIndex];

                        model.subNetNodes.xpush(n);

                        if (hops === 0) {
                            return;
                        };

                        for (var i = 0; i < model.graph.links.length; i++) {

                            if (currentIndex === model.graph.links[i].source) {
                                model.linkStrings.xpush(JSON.stringify(model.graph.links[i]));
                                this.getSubnet(model.graph.links[i].target, hops - 1)
                            };
                            if (currentIndex === model.graph.links[i].target) {
                                model.linkStrings.xpush(JSON.stringify(model.graph.links[i]));
                                this.getSubnet(model.graph.links[i].source, hops - 1)
                            };
                        };
                    },

                    click: function(d) {
                        //console.log(d);
                        var nodeName;

                        if (d.hasOwnProperty('node')) {
                            // the callback route
                            nodeName = d.node.label.name;
                        } else {
                            nodeName = d.name;
                        };

                        $("#search").val(nodeName);

                        // graph refreshed onces after nodes is added then after links
                        // prevents wild variations in graph render.
                        model.linkStrings = []; // var to ensure links no repeated

                        this.removeAllNodes(model.subNetNodes); // clears force.nodes()
                        this.removeAllLinks(model.subNetLinks); // clears force.links()

                        this.removeAllNodes(model.labelAnchors);
                        this.removeAllLinks(model.labelAnchorLinks);

                        var link,
                            source,
                            target;

                        // first the nodes and anchors
                        // extract subnet around 'd' with all nodes up to 2 hops away
                        this.getSubnet(this.findNodeIndex(nodeName, model.graph.nodes), config.hops);
                        this.createAnchors();

                        view.render();


                        // now the links and anchor links
                        // add links incrementaly
                        for (var i = 0; i < model.linkStrings.length; i++) {
                            link = JSON.parse(model.linkStrings[i]);

                            source = model.graph.nodes[link.source];
                            target = model.graph.nodes[link.target];
                            this.addLink(source.name, target.name, 2);

                        };

                        this.createAnchorLinks();

                        view.render();

                        // console.log(JSON.stringify(model.subNetNodes));
                        // console.log(JSON.stringify(model.subNetLinks));
                    }

                };

                var view = {

                    init: function() {
                        d3.select(window).on("resize", this.resize)

                        this.color = d3.scale.category10();

                        this.viz = d3.select(current_selection)
                            .append("svg:svg")
                            .attr("width", config.width)
                            .attr("height", config.height)
                            .attr("id", "svg")
                            .call(d3.behavior.zoom())
                            .attr("pointer-events", "all")
                            .attr("viewBox", "0 0 " + 1200 + " " + 500)
                            .attr("perserveAspectRatio", "xMinYMid")
                            .append('svg:g');

                        //Per-type markers, as they don't inherit styles.
                        this.viz.insert("defs")
                            .selectAll("marker")
                            .data(["suit", "licensing", "resolved"])
                            .enter()
                            .append("marker")
                            .attr("id", function(d) {
                                return d;
                            })
                            .attr("viewBox", "0 -5 10 10")
                            .attr("refX", 5)
                            .attr("refY", 0)
                            .attr("markerWidth", 6)
                            .attr("markerHeight", 6)
                            .attr("orient", "auto")
                            .append("path")
                            .attr("d", "M0,-1L5,0L0,1");
                        //.attr("M0,-5L10,0L0,5");

                        // linear gradient for the lines
                        d3.select("defs")
                            .insert("linearGradient")
                            .attr("id", "linearGradient")
                            .attr("x1", "0%")
                            .attr("y1", "0%")
                            .attr("x2", "100%")
                            .attr("y2", "100%")
                            .attr("spreadMethod", "pad");

                        d3.select("linearGradient")
                            .insert("stop")
                            .attr("offset", "0%")
                            .attr("stop-color", "grey")
                            .attr("stop-opacity", "0");

                        d3.select("linearGradient")
                            .insert("stop")
                            .attr("offset", "100%")
                            .attr("stop-color", "grey")
                            .attr("stop-opacity", "1");

                        // female D54A5C
                        // male A2C1D5
                        // clear search box
                        $("#search").val('');

                        // bind search values do the search box
                        $("#search").autocomplete({
                            source: model.nodeNames,

                            select: function(event, ui) {
                                event.preventDefault();
                                //console.log(+ui.item.value);
                                controller.click(controller.graphNodes()[+ui.item.value], +ui.item.value);
                                $("#search").val(ui.item.label);
                            },

                            focus: function(event, ui) {
                                event.preventDefault();
                                $("#search").val(ui.item.label);
                            }
                        });
                    },

                    resize: function() {
                        x = window.innerWidth || e.clientWidth || g.clientWidth;
                        y = window.innerHeight || e.clientHeight || g.clientHeight;

                        d3.select("svg").attr("width", x).attr("height", y);
                    },

                    render: function() {

                        // join
                        var link = view.viz.selectAll("line")
                            .data(model.subNetLinks, function(d) {
                                return d.source.name + "-" + d.target.name;
                            });

                        // enter
                        link.enter().insert("line", "g")
                            .attr("id", function(d) {
                                return d.source.name + "-" + d.target
                                    .name;
                            })
                            .attr("stroke-width", function(d) {
                                return d.value / 10;
                            })
                            .attr("stroke", "grey")
                            .attr("opacity", "0.5")
                            .attr("class", "link")
                            .attr("marker-end", "url(#suit)");
                        //.attr("stroke", "url(#linearGradient)")

                        // update
                        link.append("title")
                            .text(function(d) {
                                return d.value;
                            });

                        // exit
                        link.exit().remove();

                        // join
                        var node = this.viz.selectAll("g.node")
                            .data(model.subNetNodes, function(d) {
                                return d.name;
                            });

                        // enter
                        var nodeEnter = node.enter()
                            .append("g")
                            .attr("class", "node");


                        // enter
                        nodeEnter
                            .append("svg:circle")
                            .attr("r", 0)
                            .attr("id", function(d) {
                                return "Node;" + d.name;
                            })
                            .attr("class", "nodeStrokeClass")
                            .attr("fill", function(d) {
                                return view.color(d.group);
                            });

                        // exit
                        node.exit().remove();

                        // Force2 labels

                        // join
                        var anchorLink = this.viz.selectAll("line.anchorLink")
                            .data(model.labelAnchorLinks); //.enter().append("svg:line").attr("class", "anchorLink").style("stroke", "#999");

                        // join
                        var anchorNode = this.viz.selectAll("g.anchorNode")
                            .data(model.labelAnchors, function(d, i) {
                                //console.log(d.node.label.name + d.type);
                                return d.node.label.name + d.type;
                            });

                        // enter
                        var anchorNodeEnter = anchorNode
                            .enter()
                            .append("svg:g")
                            .attr("class", "anchorNode");

                        anchorNodeEnter
                            .on('click', function(d) {
                                controller.click(d);
                            }, false)

                        // enter
                        anchorNodeEnter
                            .append("svg:circle")
                            .attr("r", 0)
                            .style("fill", "red");

                        // enter
                        anchorNodeEnter
                            .append("svg:text")
                            .text(function(d, i) {
                                return i % 2 == 0 ? "" : d.node.label.name
                            })
                            .attr("class", "textClass")
                            .style("fill", "black")
                            .style("font-family", "Arial")
                            .style("font-size", 20);

                        // add coloured box around text
                        anchorNode.each(function(d, i) {
                            if (i % 2 != 0) {
                                // prevents two rects being added
                                // due to render being called twice in
                                // click func.
                                //console.log(this.childNodes[2]);
                                var textElem = this.childNodes[1].getBBox();
                                //console.log(textElem);
                                if (this.childNodes.length === 2) {
                                    d3.select(this)
                                        .insert("rect", "text")
                                        .attr("width", textElem.width)
                                        .attr("height", textElem.height)
                                        .attr("y", textElem.y)
                                        .attr("x", textElem.x)
                                        .attr("fill", function(d) {
                                            return view.color(d.node.label.group);
                                        })
                                        .attr("opacity", "0.3");
                                };

                            };
                        });


                        // exit
                        anchorNode.exit().remove();

                        // Restart the force layout.
                        model.force
                            .size([config.width, config.height])
                            .charge(-3000)
                            .gravity(1)
                            .linkDistance(50)
                            .start();

                        // restart the labels force layout
                        model.force2
                            .size([config.width, config.height])
                            .gravity(0)
                            .linkDistance(0)
                            .linkStrength(8)
                            .charge(-200)
                            .start();

                        //console.log('selection', anchorNode);
                        //console.log('force datum', force2.nodes());

                        var updateLink = function() {
                            this.attr("x1", function(d) {
                                return d.source.x;
                            }).attr("y1", function(d) {
                                return d.source.y;
                            }).attr("x2", function(d) {
                                return d.target.x;
                            }).attr("y2", function(d) {
                                return d.target.y;
                            });
                        }

                        var updateNode = function() {
                            this.attr("transform", function(d) {
                                //console.log('line 398',d.x, d.y);
                                return "translate(" + d.x + "," + d.y + ")";
                            });
                        }

                        model.force.on("tick", function() {

                            model.force2.start();

                            //---------
                            node.call(updateNode);

                            anchorNode.each(function(d, i) {

                                if (i % 2 == 0) {

                                    d.x = d.node.label.x;
                                    d.y = d.node.label.y;
                                } else {
                                    // get the bounding box
                                    var b = this.childNodes[1].getBBox();

                                    var diffX = d.x - d.node.label.x;
                                    var diffY = d.y - d.node.label.y;

                                    var dist = Math.sqrt(diffX * diffX + diffY * diffY);

                                    var shiftX = b.width * (diffX - dist) / (dist * 2);
                                    shiftX = Math.max(-b.width, Math.min(0, shiftX));

                                    var shiftY = 5;

                                    // move the label of the current anchor
                                    this.childNodes[1].setAttribute("transform", "translate(" + shiftX + "," + shiftY + ")");
                                    // move the coloured box of the current anchor
                                    this.childNodes[2].setAttribute("transform", "translate(" + shiftX + "," + shiftY + ")");
                                }
                            });
                            anchorNode.call(updateNode);

                            link.call(updateLink);

                            anchorLink.call(updateLink);
                        });
                        ///
                    }

                }

                // make it all go
                controller.init();
            });


        };

        chart.width = function(value) {
            if (!arguments.length) return config.width;
            config.width = value;
            return chart; // enable chaining
        };

        chart.height = function(value) {
            if (!arguments.length) return config.height;
            config.height = value;
            return chart; // enable chaining
        };

        chart.hops = function(value) {
            if (!arguments.length) return config.hops;
            config.hops = value;
            return chart; // enable chaining
        };

        return chart;

    };
})();


/*----------------------------------------------------------------------------
The code example below:
1. loads the JSON data.
2. Sets the width to 760px.
3. Set the height to 500px.
4. Attaches the cahrt to the DOM element with id #chart
*/


function networkWords(graph){
//d3.json("/graph/clustering", function(error, graph) {
  //  if (error) throw error;
   // console.log(graph)
    // Parse JSON into the correct format if needed

    var chart = d3.graphSub()
        .width(760)
        .height(500)
        .hops(2);
    //console.log(graph);

    d3.select("#chart")
        .datum(graph)
        .call(chart);
//});

}
/*

*/



/*        */

    function mostrarCards(){
            //document.getElementById("mytable").innerHTML="";
            //document.getElementById("mostrar").innerHTML="";

             //$.getJSON('/categoria/'+categoria, function(obj){

                   //console.log(obj);
                  /*  var Titles=dataToBuildACard['Titles']
                    var Links=dataToBuildACard['Links']
                    var Descriptions=dataToBuildACard['Descriptions']
                    var Images=dataToBuildACard['Images']
*/
                   var images=["http://www.razon.com.mx/IMG/arton326337.jpg","http://www.razon.com.mx/IMG/arton326337.jpg","http://www.razon.com.mx/IMG/arton326337.jpg","http://www.jornada.unam.mx/ultimas/2016/12/04/defender-la-patria-y-el-socialismo-juramento-en-cuba/cuba.jpg","http://www.jornada.unam.mx/tempweb/bannerelecciones2016.jpg"]


                   for (var i=1; i<5;i++){
                       //$("#card"+i.toString()).append("TOPIC: "+i.toString());
                       for (var j=0; j<images.length;j++){
                           var src=images[i];
                           var card_title="";
                           var card_text="This is a longer card with supporting text below as a natural lead-in to additional content. This content is a little bit longer.";
                           var linkBoton="#";
                           var tbl=$('<div class="card"><img class="card-img-top" src="'+src+'" alt="Card image cap" WIDTH=319px HEIGHT=180px BORDER=2 ALT="Obra de K. Haring" ><div class="card-block">    <h4 class="card-title">'+card_title+'</h4><p class="card-text">'+card_text+'</p><p class="card-text"><small class="text-muted">Last updated 3 mins ago</small> </p><a href="'+linkBoton+'" class="btn btn-primary">Go</a></div>');
                           $("#cardT"+i.toString()).append(tbl);
                       }

                   }









      }//);
      //}
