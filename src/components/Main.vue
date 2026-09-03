<script>
import Title from './sections/Title.vue'
import Abstract from './sections/Abstract.vue'
import Motivation from './sections/Motivation.vue'
import Method from './sections/Method.vue'
import ExperimentLibero from './sections/ExperimentLibero.vue'
import ExperimentReal from './sections/ExperimentReal.vue'
import ExperimentCalvin from './sections/ExperimentCalvin.vue'
import Citation from './sections/Citation.vue'
import DemoLibero from './sections/DemoLibero.vue'
import DemoReal from './sections/DemoReal.vue'
import DemoCalvin from './sections/DemoCalvin.vue'
import Video from './sections/Video.vue'
import ExperimentAttention from './sections/ExperimentAttention.vue'
import Highlights from './sections/Highlights.vue'
import Poster from './sections/Poster.vue'
import Footer from './sections/Footer.vue'

export default {
  components: {
    Title,
    Abstract,
    Motivation,
    Method,
    ExperimentLibero,
    ExperimentReal,
    ExperimentCalvin,
    Citation,
    DemoLibero,
    DemoReal,
    DemoCalvin,
    Video,
    ExperimentAttention,
    Highlights,
    Poster,
    Footer,
  }
}
</script>

<template>
  <Title/>
  <Highlights/>
  <Video/>
  <DemoReal/>
  <DemoLibero/>
  <DemoCalvin/>
  <Poster/>
  <Abstract/>
  <Motivation/>
  <Method/>
  <ExperimentReal/>
  <ExperimentLibero/>
  <ExperimentCalvin/>
  <ExperimentAttention/>
  <Citation/>
  <Footer/>
</template>
