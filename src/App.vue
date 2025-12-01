<script>

import Main from './components/Main.vue'

export default {
  components: {
    Main,
  }
}

</script>

<template>
    <div>
      
      <el-container>
        <el-main><Main/></el-main>
      </el-container>
      
      <!-- 回到顶部 -->
      <el-backtop :right="40" :bottom="80" />
    </div>
</template>

<style>

h1 {
  font-family: 'Google Sans', sans-serif;
  letter-spacing: 0px;
  font-size: 28px;
  margin: 0px;
  text-align: center;
}

h2, h3, h4, h5, h6 {
  font-family: 'Google Sans', sans-serif;
  letter-spacing: 0px;
}

.el-header {
  padding: 0px;
}

.el-footer {
  padding: 0px;
}

div {
  font-family: 'Noto Sans', sans-serif;
}

p, li {
  font-family: 'Noto Sans', sans-serif;
  font-size: 16px;
  line-height: 1.75rem;
  text-align: justify;
  text-align-last: start;
  word-spacing: normal;
  hyphens: auto;
  color: #4a4a4a;
}

code {
  font-family: 'Consolas', monospace;
  border-radius: 5px;
  padding: 2px 5px;
  background: #f2f2f2;
  color: black;
}

pre {
  border-radius: 5px;
  padding: 10px;
  background: #f2f2f2;
  line-height: 1.4rem;
}

pre:not(pre[id=bibtex]) {
  overflow-x: auto;
}

pre code {
  font-size: 16px;
  color: black;
  border: none;
  padding: 0px;
}

blockquote {
  border-left: 5px solid #bcbcbc;
  padding: 10px 20px 10px 20px;
  margin: 0px;
  background: #f6f6f6;
}

blockquote > p {
  margin-block-start: 0.5em;
  margin-block-end: 0.5em;
}

/* 链接颜色装饰 */
a {
  color: #3273dc;
  text-decoration: none;
}

/* 鼠标焦点悬浮在链接上的颜色装饰 */
a:hover {
  color: #848484;
  border-bottom: dotted;
}

p > img {
  width: 80%;
  display: block;
  margin: 0 auto;
  border-radius: 10px;
  box-shadow: 1px 1px 4px 1px #afafaf;
}

table {
  border-collapse: collapse;
  width: max-content;
  max-width: 100%;
  margin: 0 auto;
  display:block;
  overflow-x:auto;
}

thead {
  border-bottom-width: 1px;
  border-top-width: 2px;
  border-left-width: 0px;
  border-right-width: 0px;
  border-style: solid;
  border-color: rgb(0 0 0);
}

tbody tr:last-child {
  border-bottom-width: 2px;
  border-top-width: 0px;
  border-left-width: 0px;
  border-right-width: 0px;
  border-style: solid;
  border-color: rgb(0 0 0);
}

th, td {
    padding-left: 1rem;
    padding-right: 1rem;
}

.katex-display {
  overflow-x: auto;
  overflow-y: hidden;
}

</style>