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
            "name": "π0-FAST: Cookies Towel",
            "path": "./videos/main/real/baseline/cookies_towel_thumb.gif",
        },
        {
            "name": "Ours: Cookies Towel",
            "path": "./videos/main/real/inspire/cookies_towel_thumb.gif",
        },
        {
            "name": "π0-FAST: Left Bowl Middle",
            "path": "./videos/main/real/baseline/left_bowl_on_middle_bowl_thumb.gif",
        },
        {
            "name": "Ours: Left Bowl Middle",
            "path": "./videos/main/real/inspire/left_bowl_on_middle_bowl_thumb.gif",
        },
        {
            "name": "π0-FAST: Blue Cup Plate",
            "path": "./videos/main/real/baseline/blue_cup_plate_thumb.gif",
        },
        {
            "name": "Ours: Blue Cup Plate",
            "path": "./videos/main/real/inspire/blue_cup_plate_thumb.gif",
        },
        {
            "name": "π0-FAST: Pull Bottom Plate",
            "path": "./videos/main/real/baseline/pull_bottom_plate_thumb.gif",
        },
        {
            "name": "Ours: Pull Bottom Plate",
            "path": "./videos/main/real/inspire/pull_bottom_plate_thumb.gif",
        }
      ],
      imagesUnseen: [
        {
            "name": "π0-FAST: Pick Orange",
            "path": "./videos/main/real/baseline/pick_orange_thumb.gif",
        },
        {
            "name": "Ours: Pick Orange",
            "path": "./videos/main/real/inspire/pick_orange_thumb.gif",
        },
        {
            "name": "π0-FAST: Banana Towel",
            "path": "./videos/main/real/baseline/banana_towel_thumb.gif",
        },
        {
            "name": "Ours: Banana Towel",
            "path": "./videos/main/real/inspire/banana_towel_thumb.gif",
        },
        {
            "name": "π0-FAST: Ball Book",
            "path": "./videos/main/real/baseline/ball_book_thumb.gif",
        },
        {
            "name": "Ours: Ball Book",
            "path": "./videos/main/real/inspire/ball_book_thumb.gif",
        },
        {
            "name": "π0-FAST: Orange Cup Plate",
            "path": "./videos/main/real/baseline/orange_cup_plate_thumb.gif",
        },
        {
            "name": "Ours: Orange Cup Plate",
            "path": "./videos/main/real/inspire/orange_cup_plate_thumb.gif",
        }
      ],
    }
  }
}
</script>

<template>
  <el-row class="swiper-box" justify="center" v-animate-onscroll="'animated fadeInUp'">
    <!-- <el-col :xs="28" :sm="24" :md="20" :lg="16" :xl="12"> -->
    <el-col :xs="32" :sm="28" :md="24" :lg="20" :xl="16">
      <!-- 设置轮播图：循环播放、首张图序号、响应式、导航和分页、自动播放 -->
      <div class="caption-text">Seen tasks from Real-world.</div>
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
      <div class="caption-text">Unseen tasks from Real-world.</div>
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
        <swiper-slide v-for="(image, index) in imagesUnseen" :key="index">
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
  padding-bottom: 20px;
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