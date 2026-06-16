<template>
  <div class="login-body">
    <!-- 左侧：球体装饰 -->
    <div class="login-body__left" :class="{ 'animate-in': visible }">
      <img src="/login_29/qiu-4c4931db.png" alt="" class="login-body__sphere" />
    </div>

    <!-- 右侧：登录区域 -->
    <div class="login-body__right">
      <div class="login-body__digital-bg"></div>

      <!-- 标题 -->
      <div class="login-title" :class="{ 'animate-in': visible }">
        <p>桂收 · 甘蔗专用版</p>
      </div>

      <!-- 登录卡片 -->
      <div class="login-card" :class="{ 'animate-in': visible }">
        <!-- 四角装饰 -->
        <div class="login-card__corner-mark">
          <img class="login-card__corner login-card__corner--tl" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADEAAAAxCAYAAABznEEcAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyZpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDYuMC1jMDA2IDc5LmRhYmFjYmIsIDIwMjEvMDQvMTQtMDA6Mzk6NDQgICAgICAgICI+IDxyZGY6UkRGIHhtbG5zOnJkZj0iaHR0cDovL3d3dy53My5vcmcvMTk5OS8wMi8yMi1yZGYtc3ludGF4LW5zIyI+IDxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PSIiIHhtbG5zOnhtcD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wLyIgeG1sbnM6eG1wTU09Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS8iIHhtbG5zOnN0UmVmPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvc1R5cGUvUmVzb3VyY2VSZWYjIiB4bXA6Q3JlYXRvclRvb2w9IkFkb2JlIFBob3Rvc2hvcCAyMi40IChNYWNpbnRvc2gpIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOkE3MEE5NDkwRDJBRjExRURCMUREQkUyN0JENjU3OTY0IiB4bXBNTTpEb2N1bWVudElEPSJ4bXAuZGlkOkE3MEE5NDkxRDJBRjExRURCMUREQkUyN0JENjU3OTY0Ij4gPHhtcE1NOkRlcml2ZWRGcm9tIHN0UmVmOmluc3RhbmNlSUQ9InhtcC5paWQ6QTcwQTk0OEVEMkFGMTFFREIxRERCRTI3QkQ2NTc5NjQiIHN0UmVmOmRvY3VtZW50SUQ9InhtcC5kaWQ6QTcwQTk0OEZEMkFGMTFFREIxRERCRTI3QkQ2NTc5NjQiLz4gPC9yZGY6RGVzY3JpcHRpb24+IDwvcmRmOlJERj4gPC94OnhtcG1ldGE+IDw/eHBhY2tldCBlbmQ9InIiPz4967xOAAAAxklEQVR42uzasQnCQBiG4YukcxznsDKVuIE4go1O4hAGBAdIEXSEYGGlYJk0knyHEUTELsUHb+Atkqse8h8pLsl417TB92rUKjUGVCpTp5EpYK8mERBv3BBPtVZT9Xg/dBqnm5qr4/eCC6Lo5//6a/EfInF5Ra4bGwQIECBAgAABAgQIECBAgAABAgQIECBAgAABAsRQiNIdcQ+vQz5bRDwnXqiLM2KjDs57Ildb541d9WPUuiJqNQsf/0o4Ipbq7Pyd6AQYAIm0G0k0To3RAAAAAElFTkSuQmCC" alt="">
          <img class="login-card__corner login-card__corner--tr" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADEAAAAxCAYAAABznEEcAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyZpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDYuMC1jMDA2IDc5LmRhYmFjYmIsIDIwMjEvMDQvMTQtMDA6Mzk6NDQgICAgICAgICI+IDxyZGY6UkRGIHhtbG5zOnJkZj0iaHR0cDovL3d3dy53My5vcmcvMTk5OS8wMi8yMi1yZGYtc3ludGF4LW5zIyI+IDxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PSIiIHhtbG5zOnhtcD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wLyIgeG1sbnM6eG1wTU09Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS8iIHhtbG5zOnN0UmVmPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvc1R5cGUvUmVzb3VyY2VSZWYjIiB4bXA6Q3JlYXRvclRvb2w9IkFkb2JlIFBob3Rvc2hvcCAyMi40IChNYWNpbnRvc2gpIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOkE3MEE5NDk0RDJBRjExRURCMUREQkUyN0JENjU3OTY0IiB4bXBNTTpEb2N1bWVudElEPSJ4bXAuZGlkOkE3MEE5NDk1RDJBRjExRURCMUREQkUyN0JENjU3OTY0Ij4gPHhtcE1NOkRlcml2ZWRGcm9tIHN0UmVmOmluc3RhbmNlSUQ9InhtcC5paWQ6QTcwQTk0OTJEMkFGMTFFREIxRERCRTI3QkQ2NTc5NjQiIHN0UmVmOmRvY3VtZW50SUQ9InhtcC5kaWQ6QTcwQTk0OTNEMkFGMTFFREIxRERCRTI3QkQ2NTc5NjQiLz4gPC9yZGY6RGVzY3JpcHRpb24+IDwvcmRmOlJERj4gPC94OnhtcG1ldGE+IDw/eHBhY2tldCBlbmQ9InIiPz6Yc3m7AAAA0ElEQVR42uzaIQoCURSF4asYBHejSXABFptRo80tGARXYDW5iAmCCzAo7kARbArTxCLjeaDFINg8w3/hT1PmY7gz4U2lsbyPImKu6mE6VbVQHXV0RqTZqZbKnBFpctVTE/VwRaQp1Ex11cUV8Z61aqqNA6L25dpZtf/sfotfnkQ47wQIECBAgAABAgQIECBAgAABAgQIECBAgAABAgSIEiK2ZUD01dUdcVKD+Dhnd9yJlZqWYbHTDwOZOyKdZw/Vwf0Vm78W/eb+ndir8VOAAQAE0RwXVldozAAAAABJRU5ErkJggg==" alt="">
          <img class="login-card__corner login-card__corner--bl" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADEAAAAxCAYAAABznEEcAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyZpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDYuMC1jMDA2IDc5LmRhYmFjYmIsIDIwMjEvMDQvMTQtMDA6Mzk6NDQgICAgICAgICI+IDxyZGY6UkRGIHhtbG5zOnJkZj0iaHR0cDovL3d3dy53My5vcmcvMTk5OS8wMi8yMi1yZGYtc3ludGF4LW5zIyI+IDxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PSIiIHhtbG5zOnhtcD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wLyIgeG1sbnM6eG1wTU09Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS8iIHhtbG5zOnN0UmVmPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvc1R5cGUvUmVzb3VyY2VSZWYjIiB4bXA6Q3JlYXRvclRvb2w9IkFkb2JlIFBob3Rvc2hvcCAyMi40IChNYWNpbnRvc2gpIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOkE3MEE5NDk4RDJBRjExRURCMUREQkUyN0JENjU3OTY0IiB4bXBNTTpEb2N1bWVudElEPSJ4bXAuZGlkOkE3MTczRTVFRDJCMDExRURCMUREQkUyN0JENjU3OTY0Ij4gPHhtcE1NOkRlcml2ZWRGcm9tIHN0UmVmOmluc3RhbmNlSUQ9InhtcC5paWQ6QTcwQTk0OTZEMkFGMTFFREIxRERCRTI3QkQ2NTc5NjQiIHN0UmVmOmRvY3VtZW50SUQ9InhtcC5kaWQ6QTcwQTk0OTdEMkFGMTFFREIxRERCRTI3QkQ2NTc5NjQiLz4gPC9yZGY6RGVzY3JpcHRpb24+IDwvcmRmOlJERj4gPC94OnhtcG1ldGE+IDw/eHBhY2tldCBlbmQ9InIiPz4ONACoAAAAvUlEQVR42uzUMQ4BURhF4TejkWiEaGViBUJhBZKRWITCMtBYglYjUc40GkugYD867p8oLMHl3OQUU36Z917WOjyWKaV9Ml6udmrsjmiqSnWdEbFCHT++LRGxUm3cEbG1mrkj8vexKpwRsY6q3RGx0S8gEggQIECAAAECBAgQIECAAAECBAgQIECAAAECBIg/Rjy/qKvqu/+Jibqpqftx6qmzWqnM+U401FadVNv9Ys/VXQ3dX6eBuqjFS4ABAEUSMspJ5fd3AAAAAElFTkSuQmCC" alt="">
          <img class="login-card__corner login-card__corner--br" src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADEAAAAxCAYAAABznEEcAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyZpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDYuMC1jMDA2IDc5LmRhYmFjYmIsIDIwMjEvMDQvMTQtMDA6Mzk6NDQgICAgICAgICI+IDxyZGY6UkRGIHhtbG5zOnJkZj0iaHR0cDovL3d3dy53My5vcmcvMTk5OS8wMi8yMi1yZGYtc3ludGF4LW5zIyI+IDxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PSIiIHhtbG5zOnhtcD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wLyIgeG1sbnM6eG1wTU09Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS8iIHhtbG5zOnN0UmVmPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvc1R5cGUvUmVzb3VyY2VSZWYjIiB4bXA6Q3JlYXRvclRvb2w9IkFkb2JlIFBob3Rvc2hvcCAyMi40IChNYWNpbnRvc2gpIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOkE3MTczRTYxRDJCMDExRURCMUREQkUyN0JENjU3OTY0IiB4bXBNTTpEb2N1bWVudElEPSJ4bXAuZGlkOkE3MTczRTYyRDJCMDExRURCMUREQkUyN0JENjU3OTY0Ij4gPHhtcE1NOkRlcml2ZWRGcm9tIHN0UmVmOmluc3RhbmNlSUQ9InhtcC5paWQ6QTcxNzNFNUZEMkIwMTFFREIxRERCRTI3QkQ2NTc5NjQiIHN0UmVmOmRvY3VtZW50SUQ9InhtcC5kaWQ6QTcxNzNFNjBEMkIwMTFFREIxRERCRTI3QkQ2NTc5NjQiLz4gPC9yZGY6RGVzY3JpcHRpb24+IDwvcmRmOlJERj4gPC94OnhtcG1ldGE+IDw/eHBhY2tldCBlbmQ9InIiPz4vu4utAAAAw0lEQVR42uzTQQqCUBSFYRUHQZMInIrtIBDaQRC0CcFtWKtoA0HNpGlLCKEFNavzQEGCBkGDDvwXftDZ+3jvxtPjIzKfOjEHlOrgjJirVk1cEeHcZ1UMP46zV5uxyG3C4Xfv1+I0Rf+MEmdE2y905IwoP225/YAAAQIECBAgQIAAAQIECBAgQIAAAQIECBAgQID4MSJXnXr+UV8h1uquVo43EatGXVXm8pzS0fdMndTWbScGxFJd1MJ1sSt1cwWEeQkwAMUaMZ6cSdfLAAAAAElFTkSuQmCC" alt="">
        </div>

        <div class="login-card__inner">
          <!-- 欢迎文字 -->
          <div class="login-card__welcome" :class="{ 'animate-in': visible }">欢迎登录系统!</div>

          <!-- 账号输入 -->
          <div class="login-card__input" :class="{ 'animate-in': visible }">
            <div class="login-card__input-icon">
              <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABcAAAAYCAYAAAARfGZ1AAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyZpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDYuMC1jMDA2IDc5LmRhYmFjYmIsIDIwMjEvMDQvMTQtMDA6Mzk6NDQgICAgICAgICI+IDxyZGY6UkRGIHhtbG5zOnJkZj0iaHR0cDovL3d3dy53My5vcmcvMTk5OS8wMi8yMi1yZGYtc3ludGF4LW5zIyI+IDxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PSIiIHhtbG5zOnhtcD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wLyIgeG1sbnM6eG1wTU09Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS8iIHhtbG5zOnN0UmVmPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvc1R5cGUvUmVzb3VyY2VSZWYjIiB4bXA6Q3JlYXRvclRvb2w9IkFkb2JlIFBob3Rvc2hvcCAyMi40IChNYWNpbnRvc2gpIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOkZBQ0ZDRDRDRDJBRDExRURCMUREQkUyN0JENjU3OTY0IiB4bXBNTTpEb2N1bWVudElEPSJ4bXAuZGlkOkZBQ0ZDRDRERDJBRDExRURCMUREQkUyN0JENjU3OTY0Ij4gPHhtcE1NOkRlcml2ZWRGcm9tIHN0UmVmOmluc3RhbmNlSUQ9InhtcC5paWQ6RkFDRkNENEFEMkFEMTFFREIxRERCRTI3QkQ2NTc5NjQiIHN0UmVmOmRvY3VtZW50SUQ9InhtcC5kaWQ6RkFDRkNENEJEMkFEMTFFREIxRERCRTI3QkQ2NTc5NjQiLz4gPC9yZGY6RGVzY3JpcHRpb24+IDwvcmRmOlJERj4gPC94OnhtcG1ldGE+IDw/eHBhY2tldCBlbmQ9InIiPz7+diGoAAABn0lEQVR42tzVSyhEURzHcWNGiSyEjaImC0U2FEIeI1nYKCELdhN2FpIsrOwoCxuy8ZqQsLJQFhayEMqGpIiVsVCUPML4/ut/6zbde+fhbjj1aU5zz/2dc++c/xlP5uJbSoxWiEHUIQM3WMcmvp1u9MQI78YC0i2u7aMdT3Y3pzoE1yKkwQfoQQsm8IJGrCW7cllZA7bQhS/TtUqdMA1NOjbulWehXvujUcHSjrCh/bZEX0uOPJX2r2zGGN/nJfPOf93+X/inqe+1GeO1GBtX+L3uZWkBmzGBGD+448pD2p+F31wbGEcNPpwKyefwysbQjCKcYwcPWlglOmYEt4mG+zX4WsPlCOiIGvOOcgSxizun8i9Anx5WZRYTRvCs1Wv1Ok+1aleNp5FwOUbn9WAyqlLK/RB7WupnCJuO2HxdQDVaUWWaMKITBCV8ks6w6bBawTYeE9jS2ehEr5770qYk/JhOBQYw50Lt9OsOO0k1/ahhlwrTyPH93bPFZ9oB8vc15EJmrn6+Svg0llDq4qJlO85I+DJkxxS7GH6Byx8BBgDeAVoVW8JiwQAAAABJRU5ErkJggg==" alt="">
            </div>
            <input
              v-model="form.name"
              type="text"
              placeholder="请输入账号"
              @keyup.enter="handleLogin"
            />
          </div>

          <!-- 密码输入 -->
          <div class="login-card__input" :class="{ 'animate-in': visible }">
            <div class="login-card__input-icon">
              <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABYAAAAXCAYAAAAP6L+eAAAAGXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyZpVFh0WE1MOmNvbS5hZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8iIHg6eG1wdGs9IkFkb2JlIFhNUCBDb3JlIDYuMC1jMDA2IDc5LmRhYmFjYmIsIDIwMjEvMDQvMTQtMDA6Mzk6NDQgICAgICAgICI+IDxyZGY6UkRGIHhtbG5zOnJkZj0iaHR0cDovL3d3dy53My5vcmcvMTk5OS8wMi8yMi1yZGYtc3ludGF4LW5zIyI+IDxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PSIiIHhtbG5zOnhtcD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wLyIgeG1sbnM6eG1wTU09Imh0dHA6Ly9ucy5hZG9iZS5jb20veGFwLzEuMC9tbS8iIHhtbG5zOnN0UmVmPSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvc1R5cGUvUmVzb3VyY2VSZWYjIiB4bXA6Q3JlYXRvclRvb2w9IkFkb2JlIFBob3Rvc2hvcCAyMi40IChNYWNpbnRvc2gpIiB4bXBNTTpJbnN0YW5jZUlEPSJ4bXAuaWlkOkZBQ0ZDRDUwRDJBRDExRURCMUREQkUyN0JENjU3OTY0IiB4bXBNTTpEb2N1bWVudElEPSJ4bXAuZGlkOkZBQ0ZDRDUxRDJBRDExRURCMUREQkUyN0JENjU3OTY0Ij4gPHhtcE1NOkRlcml2ZWRGcm9tIHN0UmVmOmluc3RhbmNlSUQ9InhtcC5paWQ6RkFDRkNENEVEMkFEMTFFREIxRERCRTI3QkQ2NTc5NjQiIHN0UmVmOmRvY3VtZW50SUQ9InhtcC5kaWQ6RkFDRkNENEZEMkFEMTFFREIxRERCRTI3QkQ2NTc5NjQiLz4gPC9yZGY6RGVzY3JpcHRpb24+IDwvcmRmOlJERj4gPC94OnhtcG1ldGE+IDw/eHBhY2tldCBlbmQ9InIiPz7JSWFIAAABIUlEQVR42mLkXviDAQ9gBOIQIM4GYnMgZgfiB0C8Goi7gfgNTo14DGYF4iVAHIZD/gUQewHxeWySTHhc2wE1FGRzBRDLAjEf1LALQCwBxFuBWIgUFysA8R0gZgZidyDehSbPBcRHgdgAiNuAuJpYF/tBDd2MxVAQ+AbElVB2KClBoQalj+AJqsNQWokUg3mg9C88Bn+F0sykRh5FgAWJloamW2QXC0EjkhCAqfkPxE+B+A8oVTgAGeuBWIBKjv0AxIEglzZADf0CxH8pNJQZalYDC5JLbaEJnxJgAM2JAqREHjcUkxR5xIBrUFqe2gbLkRImNEvHQ89gUsJ4Ba0MjiTXYHUqhIA6ssF3gVifVK8SAHdBBhdAOcrUMhRkJkCAAQCIXS9X+bIsSgAAAABJRU5ErkJggg==" alt="">
            </div>
            <input
              v-model="form.password"
              type="password"
              placeholder="密码"
              @keyup.enter="handleLogin"
            />
          </div>

          <!-- 记住密码 -->
          <div class="login-card__options" :class="{ 'animate-in': visible }">
            <el-checkbox v-model="form.remember" class="login-card__remember">记住密码</el-checkbox>
          </div>

          <!-- 登录按钮 -->
          <div
            class="login-card__btn"
            :class="{ 'animate-in': visible, 'login-card__btn--loading': loading }"
            @click="handleLogin"
          >
            <span v-if="!loading">登录</span>
            <span v-else>登录中...</span>
          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const visible = ref(false)
const loading = ref(false)

const form = reactive({
  name: '',
  password: '',
  remember: false,
})

const handleLogin = async () => {
  if (!form.name || !form.password) return
  loading.value = true
  try {
    await authStore.login(form.name, form.password)
    if (form.remember) {
      localStorage.setItem('saved_name', form.name)
    } else {
      localStorage.removeItem('saved_name')
    }
    const redirect = route.query.redirect || '/'
    router.push(redirect)
  } catch {
    // error handled by axios interceptor
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  // If already logged in, redirect
  if (authStore.isLoggedIn) {
    router.replace('/')
    return
  }
  // Restore saved username
  const savedName = localStorage.getItem('saved_name')
  if (savedName) {
    form.name = savedName
    form.remember = true
  }
  // Trigger entry animations
  requestAnimationFrame(() => {
    visible.value = true
  })
})
</script>

<style lang="scss" scoped>
/* 完整还原旧登录页样式，使用 px 单位保持与原版一致 */
.login-body {
  width: 100vw;
  height: 100vh;
  position: fixed;
  background: url('/login_29/bg-d5080e20.jpg') center center no-repeat;
  background-size: 100% 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: row;
  overflow: hidden;
}

/* 左侧球体区域 */
.login-body__left {
  width: 50%;
  height: 100%;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  opacity: 0;
  transform: translateX(-60px);
  transition: all 0.8s ease-out;

  &.animate-in {
    opacity: 1;
    transform: translateX(0);
  }
}

.login-body__sphere {
  max-width: 80%;
  max-height: 80%;
  object-fit: contain;
}

/* 右侧登录区域 */
.login-body__right {
  width: 50%;
  height: 100%;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
  z-index: 10;
}

/* 数字背景 */
.login-body__digital-bg {
  background: url('/login_29/shuzibg-1d7d8461.png') no-repeat;
  background-size: contain;
  width: 100%;
  height: 100%;
  position: absolute;
  opacity: 0.6;
  z-index: -1;
}

/* 标题 */
.login-title {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  margin-bottom: 30px;
  opacity: 0;
  transform: translateY(-30px);
  transition: all 0.6s ease-out 0.3s;

  &.animate-in {
    opacity: 1;
    transform: translateY(0);
  }

  p {
    font-size: 36px;
    font-weight: 400;
    color: #00bff4;
    margin: 0;
    font-family: 'PangMenZhengDao', 'Microsoft YaHei', sans-serif;
    background: linear-gradient(90deg, #009FF1 0%, #00E8CF 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
}

/* 登录卡片 */
.login-card {
  width: 420px;
  background: rgba(32, 163, 245, 0.1);
  display: flex;
  min-height: 280px;
  justify-content: flex-start;
  border: 1px solid rgb(17, 107, 178);
  align-items: center;
  flex-direction: column;
  padding-bottom: 30px;
  position: relative;
  opacity: 0;
  transform: translateX(60px);
  transition: all 0.8s ease-out 0.5s;

  &.animate-in {
    opacity: 1;
    transform: translateX(0);
  }
}

/* 四角装饰 */
.login-card__corner-mark {
  position: absolute;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
}

.login-card__corner {
  position: absolute;
  width: 28px;
  height: 28px;

  &--tl {
    top: -1px;
    left: -1px;
  }
  &--tr {
    top: -1px;
    right: -1px;
  }
  &--bl {
    bottom: -1px;
    left: -1px;
  }
  &--br {
    bottom: -1px;
    right: -1px;
  }
}

.login-card__inner {
  width: 360px;
  position: relative;
  z-index: 1;
  padding-top: 20px;
}

/* 欢迎文字 */
.login-card__welcome {
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
  font-weight: 400;
  color: #34dcfc;
  font-size: 22px;
  height: 60px;
  display: flex;
  justify-content: center;
  align-items: center;
  opacity: 0;
  transform: translateY(-20px);
  transition: all 0.6s ease-out 0.8s;

  &.animate-in {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 输入框 */
.login-card__input {
  width: 100%;
  display: flex;
  justify-content: flex-start;
  align-items: center;
  background: rgba(24, 80, 136, 0.4);
  margin-bottom: 16px;
  position: relative;
  height: 44px;
  border: 1px solid rgba(32, 163, 245, 0.4);
  opacity: 0;
  transform: translateX(-40px);
  transition: all 0.6s ease-out;

  &:nth-child(2) {
    transition-delay: 1.2s;
  }
  &:nth-child(3) {
    transition-delay: 1.5s;
  }

  &.animate-in {
    opacity: 1;
    transform: translateX(0);
  }

  &:focus-within {
    border-color: rgba(32, 163, 245, 0.8);
    box-shadow: 0 0 8px rgba(32, 163, 245, 0.2);
  }
}

.login-card__input-icon {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 50px;
  flex-shrink: 0;

  img {
    width: 18px;
  }
}

.login-card__input input {
  width: 100%;
  background: none;
  height: 44px;
  border: none;
  color: #fff;
  outline: none;
  font-size: 14px;
  font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
  font-weight: 700;

  &::placeholder {
    color: rgba(255, 255, 255, 0.7);
  }
}

/* 记住密码 & 忘记密码 */
.login-card__options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 50px;
  opacity: 0;
  transform: translateX(-40px);
  transition: all 0.6s ease-out 1.8s;

  &.animate-in {
    opacity: 1;
    transform: translateX(0);
  }
}

.login-card__remember {
  :deep(.el-checkbox__label) {
    color: #fff;
    font-size: 12px;
  }
  :deep(.el-checkbox__inner) {
    background: transparent;
    border-color: rgba(32, 163, 245, 0.6);
  }
  :deep(.el-checkbox__input.is-checked .el-checkbox__inner) {
    background: rgba(32, 163, 245, 0.3);
    border-color: #20A3F5;
  }
  :deep(.el-checkbox__input.is-checked + .el-checkbox__label) {
    color: #34dcfc;
  }
}

/* 登录按钮 */
.login-card__btn {
  width: 100%;
  height: 44px;
  font-size: 22px;
  font-weight: 400;
  color: #fff;
  background: #20A3F5;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  letter-spacing: 20px;
  text-indent: 20px;
  transition: all 0.3s ease;
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.6s ease-out 2.1s;

  &.animate-in {
    opacity: 1;
    transform: translateY(0);
  }

  &:hover {
    background: #1b8fd4;
    box-shadow: 0 0 15px rgba(32, 163, 245, 0.4);
  }

  &:active {
    background: #1780c0;
  }

  &--loading {
    pointer-events: none;
    opacity: 0.7;
  }
}
</style>
