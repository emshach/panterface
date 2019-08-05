<template lang="html">
  <div class="collection-view">
    
  </div>
</template>

<script lang="js">
import { FilterInput, ActionsInput } from '@/components'
import { FilteredMixin, ActionsMixin } from '@/lib/mixins'

export default {
  name: "CollectionView",
  mixins: [ FilteredMixin, ActionsMixin ],
  components: {
    FilterInput,
    ActionsInput,
  },
  props: {},
  data() {
    return {
    };
  },
  created() {},
  mounted() {},
  methods: {},
  computed: {}
}
</script>

<style lang="scss">
.collection-view {
  
}
</style>
