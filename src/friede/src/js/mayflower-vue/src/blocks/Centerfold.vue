<template lang="html">
  <vue-glide v-if="content.length" type="carousel">
  </vue-glide>
  <div v-else class="glide-slideshow empty" />
</template>

<script lang="js">
import { Glide as VueGlide, GlideSlider } from 'vue-glide-js'
import 'vue-glide-js/dist/vue-glide.css'

Vue.use( VueGlide );

export default  {
  name: 'centerfold',
  components: { VueGlide, GlideSlider },
  props: {
    content: {
      type: Array,
      default: () => []
    }
  },
  mounted() {
    
  },
  data() {
    return {
      
    }
  },
  methods: {
    
  },
  computed: {
    
  }
}
</script>

<style scoped lang="scss">
.centerfold {
  
}
</style>
