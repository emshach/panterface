<template lang="html">
  <span class="json-array">
    <span class="json-delim">[</span>
    <vk-btn v-if="intlVal.length > 1" class="json-collapse" type="light"
            @click.prevent="collapse=!collapse">
      <font-awesome-icon :icon="collapse ? 'plus' : 'minus' " />
    </vk-btn>
    <span v-if="collapse" class="json-array-content">...</span>
    <span v-else class="json-array-content">
      <template v-for="( v, i ) in intlVal">
        <json-widget :readonly="readonly" :edit="editMode" :key="i"
                     v-model="v.data" @input="input" />
      </template>
      <vk-btn v-if="editing" class="json-add" type="light" @click.prevent="addElem">
        <font-awesome-icon icon="plus" />
      </vk-btn>
    </span>
    <span class="json-delim">]</span>
  </span>
</template>

<script lang="js">
import { Button as VkBtn } from 'vuikit/lib/button'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faPlus, faMinus } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { JsonWidgetMixin } from '@/lib/mixins'

library.add( faPlus, faMinus )

export default  {
  name: 'JsonArray',
  mixins: [ JsonWidgetMixin ],
  components: {
    VkBtn,
    FontAwesomeIcon,
  },
  props: {
    value: {
      type: Array,
      default: () => []
    }
  },
  mounted() {
    this.updateVal();
  },
  data() {
    return {
      intlVal: [],
      collapse: false,
    }
  },
  methods: {
    updateVal() {
      this.intlVal = this.value.map( x => ({ data: x }))
    },
    input() {
      this.$emit( 'input', this.intlVal.map( x => x.data ));
    },
    addElem() {
      this.intlVal.push({ data: null });
    }
  },
  computed: {
  },
  watch: {
    value( val ) {
      this.updateVal();
    }
  }
}
</script>

<style lang="scss">
.json-array {
  .json-array-content > .json-widget {
    display: block;
    margin-left: 1em;
  }
}
</style>
