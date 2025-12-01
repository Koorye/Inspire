<script setup>
import motivation from '../mds/motivation.mdx';
</script>

<template>
  <div v-animate-onscroll="'animated fadeInUp'">
    <el-divider />

    <el-row justify="center">
        <el-col :xs="28" :sm="24" :md="20" :lg="16" :xl="12">
          <h1 class="title">Motivation</h1>
          <el-image src="./motivation.png" class="caption-img" fit="cover" />
          <motivation class="caption-text" />
        </el-col>
    </el-row>

  </div>
</template>

<style scoped>

.title {
  margin-bottom: 20px;
}

.caption-text {
    margin: 20px 0;
}

</style>