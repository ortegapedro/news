var app = angular.module('app', [
    'angular-jqcloud'
  ]);

  app.controller('controller', function($scope) {
    $scope.words = [
      
      {text: "7", weight: 628,link: 'https://www.google.com.mx/search?q=galaxy'},
      {text: "galaxy", weight: 498},
      {text: "note", weight: 465},
      {text: "samsung", weight: 436},
      {text: "nuevo", weight: 424},
      {text: "google", weight: 420},
      {text: "años", weight: 391},
      {text: "personas", weight: 278},
      {text: "apple", weight: 276},
      {text: "video", weight: 266},
      {text: "equipo", weight: 276},
      {text: "usuarios", weight: 266},
      {text: "millones", weight: 250},
      {text: "modelo", weight: 249},
      {text: "méxico", weight: 238},
      {text: "mil", weight: 230},
      {text: "espacial", weight: 229},
      {text: "nasa", weight: 227},
      {text: "sep", weight: 226},
      {text: "mundo", weight: 221},      
      {text: "lanzamiento", weight: 219},
      {text: "nuño", weight: 209},
      {text: "marte", weight: 200},
      {text: "facebook", weight: 200},
      {text: "unam", weight: 197},
      {text: "iphone", weight: 193}
    ];
    
    $scope.colors = ["#800026", "#bd0026", "#e31a1c", "#fc4e2a", "#fd8d3c", "#feb24c", "#fed976"];
    
    $scope.update = function() {
      $scope.words.splice(-5);
    };
  });