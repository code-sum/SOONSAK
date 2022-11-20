//주의 : hTML에서 보여지는 이미지 크기가 본래 이미지 크기보다 작아야 함. ( width , height )
window.onload = function () {
  $(".wrap")
    .on('mousemove', magnify)
    .prepend("<div class='magnifier'></div>")
    .children('.magnifier').css({
      "background": "url('" + $(".target").attr("src") + "') no-repeat"
    });

  var target = $('.target');
  var magnifier = $('.magnifier');

  function magnify(e) {

    // 마우스 위치에서 .magnify의 위치를 차감해 컨테이너에 대한 마우스 좌표를 얻는다.
    var mouseX = e.pageX - $(this).offset().left;
    var mouseY = e.pageY - $(this).offset().top;

    // 컨테이너 밖으로 마우스가 벗어나면 돋보기를 없앤다.
    if (mouseX < $(this).width() && mouseY < $(this).height() && mouseX > 0 && mouseY > 0) {
      magnifier.fadeIn(100);
    }
    else {
      magnifier.fadeOut(100);
    }

    //돋보기가 존재할 때
    if (magnifier.is(":visible")) {

      /* 이미지에 대한 마우스 포인터 아래의 픽셀 비율(본래 이미지 크기에 대한)을 얻고 
      이를 사용하여 돋보기 내부에 큰 이미지를 배치한다. */
      var rx = -(mouseX / target.width() * target[0].naturalWidth - magnifier.width() / 2);
      var ry = -(mouseY / target.height() * target[0].naturalHeight - magnifier.height() / 2);

      //돋보기를 마우스 위치에 따라 움직인다.
      //돋보기의 width, height 절반을 마우스 좌표에서 차감해 마우스와 돋보기 위치를 일치시킨다.
      var px = mouseX - magnifier.width() / 2;
      var py = mouseY - magnifier.height() / 2;

      //적용
      magnifier.css({
        left: px,
        top: py,
        backgroundPosition: rx + "px " + ry + "px"
      });
    }
  }
};