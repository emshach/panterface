<template lang="html">
  <div class="switchboard">
    <transition mode="in-out">
      <div class="display" v-if="matches.length || locations.length">
        <ul>
          <li v-for="match in matches">{{ match }}</li>
        </ul>
      </div>
    </transition>
  </div>
</template>

<script lang="js">
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
    bottom: 30px;
    left: 10px;
    right: 10px;
    background: rgba(0,0,0,0.75);
    color: white;
  }
}
</style>
