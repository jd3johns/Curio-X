
$(document).ready(function () {

    $( ".loginButton" ).click(function() {
    //TODO

    });

    $( ".beginButton" ).click(function() {
      // $("#beginButton").animate({
      //   width: "200px",
      //   height: "200px",
      //   },500);
      // $( this ).css({'border-radius':'100px','width':'100px', 'height':'100px'});
        $ ("body").css({'background-color':'#dadede', 'color':'#dadede'});
        $ ("h1").css({'border':'none'});
        $ (".header").css({'display':'none'})
        $ (".footer").css({'border':'none'}).delay(250)
        // window.location("http://www.w3schools.com", _self);
        .queue( function(next){ 
    //          $(".title").css({'transition': '0.1s','height':'70px', 'line-height':'70px', 'font-size':'3em'});
    //           $(".header").css({'height':'108px'});
    
            window.open("game.html", "_self");
            next(); 
        });

        // $ (".container").css({'display':'none'});
    });


    $(document).scroll(function() {
    })
    
});

