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
            "name": "miniVLA-VQ: Butter Drawer",
            "path": "./videos/main/libero/baseline/90_butter_drawer.gif",
        },
        {
            "name": "Ours: Butter Drawer",
            "path": "./videos/main/libero/inspire/90_butter_drawer.gif",
        },
        {
            "name": "miniVLA-VQ: Moka Stove",
            "path": "./videos/main/libero/baseline/90_moka_stove.gif",
        },
        {
            "name": "Ours: Moka Stove",
            "path": "./videos/main/libero/inspire/90_moka_stove.gif",
        },
        {
            "name": "miniVLA-VQ: Sauce Tray",
            "path": "./videos/main/libero/baseline/90_sauce_tray.gif",
        },
        {
            "name": "Ours: Sauce Tray",
            "path": "./videos/main/libero/inspire/90_sauce_tray.gif",
        },
        {
            "name": "miniVLA-VQ: Book Caddy",
            "path": "./videos/main/libero/baseline/90_book_caddy.gif",
        },
        {
            "name": "Ours: Book Caddy",
            "path": "./videos/main/libero/inspire/90_book_caddy.gif",
        }
      ],
      imagesUnseen: [
        {
            "name": "miniVLA-VQ: Bowl Plate",
            "path": "./videos/main/libero/baseline/goal_bowl_plate.gif",
        },
        {
            "name": "Ours: Bowl Plate",
            "path": "./videos/main/libero/inspire/goal_bowl_plate.gif",
        },
        {
            "name": "miniVLA-VQ: Cheese Basket",
            "path": "./videos/main/libero/baseline/object_cheese_basket.gif",
        },
        {
            "name": "Ours: Cheese Basket",
            "path": "./videos/main/libero/inspire/object_cheese_basket.gif",
        },
        {
            "name": "miniVLA-VQ: Bowl Plate",
            "path": "./videos/main/libero/baseline/spatial_bowl_plate.gif",
        },
        {
            "name": "Ours: Bowl Plate",
            "path": "./videos/main/libero/inspire/spatial_bowl_plate.gif",
        },
        {
            "name": "miniVLA-VQ: Book Caddy",
            "path": "./videos/main/libero/baseline/10_book_caddy.gif",
        },
        {
            "name": "Ours: Book Caddy",
            "path": "./videos/main/libero/inspire/10_book_caddy.gif",
        }
      ],
    }
  }
}
</script>

<template>
  <div v-animate-onscroll="'animated fadeInUp'">
    <el-row justify="center">
      <h1>LIBERO Demonstrations</h1>
    </el-row>

    <el-row justify="center">
    <!-- <el-col :xs="28" :sm="24" :md="20" :lg="16" :xl="12"> -->
    <el-col :xs="28" :sm="24" :md="20" :lg="16" :xl="12" class="swiper-box">
      <!-- 设置轮播图：循环播放、首张图序号、响应式、导航和分页、自动播放 -->
      <div class="caption-text">Seen tasks LIBERO-90.</div>
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
      <div class="caption-text">Unseen tasks LIBERO-Goal, LIBERO-Object, LIBERO-Spatial and LIBERO-10.</div>
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
  </div>
</template>
  
<style scoped>

.swiper-box {
    background-color: var(--pcd-surface);
  border: 1px solid var(--pcd-border);
  border-radius: 16px;
  padding: 18px 14px;
}

/* 设置Swiper风格 */
.swiper {
  --swiper-theme-color: var(--pcd-accent);
}

.swiper-slide-text {
  padding: 5px;
  font-size: 15px;
  font-weight: 500;
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