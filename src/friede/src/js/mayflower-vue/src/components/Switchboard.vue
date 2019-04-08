<template lang="html">
  <div class="switchboard">
    <transition mode="in-out">
      <vk-grid  v-if="matches.length || locations.length"
                gutter="small" class="display">
        <div v-for="match in matches">{{ match }}</div>
      </vk-grid>
    </transition>
  </div>
</template>

<script lang="js">
import { Grid } from 'vuikit/lib/grid';
export default  {
  name: 'switchboard',
  props: {
    matches: {
      type: Array,
      default: () => []
    },
    locations: {
      type: Array,
      default: () => []
    }
  },
  components: {
    'vk-grid': Grid,
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
.switchboard {
  .display{
    position: fixed;
    bottom: 42px;
    left: 10px;
    right: 10px;
    background: rgba(0,0,0,0.75);
    color: white;
    border-radius: 4px;
  }
}
</style>
