<script setup>
import experiment from '../mds/attention.mdx';
</script>

<template>
  <div v-animate-onscroll="'animated fadeInUp'">

    <el-row justify="center">
        <el-col :xs="28" :sm="24" :md="20" :lg="16" :xl="12">
            <el-image src="./attention.png" class="caption-img" fit="cover" />
            <experiment class="caption-text" />
        </el-col>
    </el-row>

  </div>
</template>

<style scoped>

.caption-img {
    width: 100%;
}

.caption-text {
    margin: 20px 0;
}

</style>