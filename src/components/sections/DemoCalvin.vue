<script>
import { Swiper, SwiperSlide} from 'swiper/vue';
import { Navigation, Pagination, Autoplay} from 'swiper/modules';
import 'swiper/css/bundle';

export default {
  components: {
      Swiper,
      SwiperSlide,
      Navigation,
      Pagination,
      Autoplay,
    },
  data() {
    return {
      modules: [
        Navigation,
        Pagination,
        Autoplay,
      ],
      // 选择要轮播的照片
      imagesSeen: [
        {
            "name": "miniVLA-VQ",
            "path": "./videos/main/calvin/seq7_success0.gif",
        },
        {
            "name": "Ours",
            "path": "./videos/main/calvin/seq7_success5.gif",
        },
        {
            "name": "miniVLA-VQ",
            "path": "./videos/main/calvin/seq179_success0.gif",
        },
        {
            "name": "Ours",
            "path": "./videos/main/calvin/seq179_success5.gif",
        }
      ]
    }
  }
}
</script>

<template>
  <el-row class="swiper-box" justify="center" v-animate-onscroll="'animated fadeInUp'">
    <!-- <el-col :xs="28" :sm="24" :md="20" :lg="16" :xl="12"> -->
    <el-col :xs="32" :sm="28" :md="24" :lg="20" :xl="16">
      <!-- 设置轮播图：循环播放、首张图序号、响应式、导航和分页、自动播放 -->
      <div class="caption-text">CALVIN ABC -> D.</div>
      <swiper
        :loop="true"
        :slidesPerView="1"
        :slides-per-group="2"
        :breakpoints="{
          600: {
            slidesPerView: 4,
            spaceBetween: 20,
          },
        }"
        :modules="modules"
        :navigation="{ 
          hideOnClick:true,
        }"
        :pagination="{ 
          hideOnClick:true,
          clickable:true, 
          type:'bullets' 
        }"
        :autoplay="{ 
          delay:5000,
          disableOnInteraction:false,
          pauseOnMouseEnter:true,
        }"
        >
        <swiper-slide v-for="(image, index) in imagesSeen" :key="index">
          <div class="swiper-slide-text">{{ image.name }}</div>
          <el-image class="swiper-img" :src="image.path" :alt="image.name" fit="contain" />
        </swiper-slide>
      </swiper>
    </el-col>
  </el-row>
</template>
  
<style scoped>

.swiper-box {
  background-color: #eeeeee;
}

/* 设置Swiper风格 */
.swiper {
  --swiper-theme-color: white;
}

.swiper-slide-text {
  padding: 5px;
  font-size: 16px;
  text-align: center;
  color: #4a4a4a;
}

.swiper-img {
  width: 100%;
  border-radius: 15px;
}

.caption-text {
  text-align: center;
  font-size: 20px;
  margin-top: 20px;
  color: #4a4a4a;
}

</style>