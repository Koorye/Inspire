<script>
</script>

<template>
  <div>
    <!-- 每个网站的视频的iframe可能不一致，最好在这里手动调整 -->
    <el-row justify="center">
      <el-col :xs="28" :sm="24" :md="20" :lg="16" :xl="12" >

        <!-- local -->
        <el-container class="video-container">
          <video autoplay controls mute>
            <source src="/Inspire.mp4" type="video/mp4">
          </video>
        </el-container>
      </el-col>
    </el-row>
  </div>
</template>

<style scoped>

.video-container{
  margin: 20px;
}

iframe, video {
  aspect-ratio: 16 / 9;
  width: 100%;
}

</style>