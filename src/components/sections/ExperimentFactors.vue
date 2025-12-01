<script setup>
import experiment from '../mds/experiment_factors.mdx';
</script>

<template>
  <div v-animate-onscroll="'animated fadeInUp'">

    <el-row justify="center">
        <el-col :xs="28" :sm="24" :md="20" :lg="16" :xl="12">
            <el-image src="./simpler_factors.png" class="caption-img" fit="cover" />
            <el-image src="./real_factors.png" class="caption-img" fit="cover" />
            <experiment class="caption-text" />
        </el-col>
    </el-row>

  </div>
</template>

<style scoped>

.caption-img {
    width: 100%;
}

</style>