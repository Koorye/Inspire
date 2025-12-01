<script setup>
import abstract from '../mds/abstract.mdx';
</script>

<template>
  <div>
    <!-- <el-divider /> -->

    <el-row class="abstract-box" justify="center" v-animate-onscroll="'animated fadeInUp'">
        <el-col :xs="28" :sm="24" :md="20" :lg="16" :xl="12">
            <abstract />
        </el-col>
    </el-row>

  </div>
</template>

<style scoped>

.abstract-box {
  margin-top: 40px;
}

</style>