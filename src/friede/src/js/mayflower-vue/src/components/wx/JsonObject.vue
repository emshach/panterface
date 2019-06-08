<template lang="html">
  <span class="json-object">
    <span class="json-delim">{</span>
    <vk-btn v-if="intlVal.length > 1" class="json-collapse" type="light"
            @click.prevent="collapse=!collapse">
      <font-awesome-icon :icon="collapse ? 'plus' : 'minus' " />
    </vk-btn>
    <span v-if="collapse" class="json-object-content">...</span>
    <span v-else class="json-object-content">
      <template v-for="v in intlVal">
        <json-tuple :readonly="readonly" :key="v.data.key" v-model="v.data"
                    @input="input" />
      </template>
      <vk-btn v-if="editing" class="json-add" type="light" @click.prevent="addTuple">
        <font-awesome-icon icon="plus" />
      </vk-btn>
    </span>
    <span class="json-delim">}</span>
  </span>
</template>

<script lang="js">
import { ButtonLink as VkBtn } from 'vuikit/lib/button'
import { JsonTuple } from './json'
import { JsonWidgetMixin } from '@/lib/mixins'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faPlus, faMinus } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add( faPlus, faMinus )

export default  {
  name: 'json-object',
  mixins: [ JsonWidgetMixin ],
  components: { VkBtn, JsonTuple },
  props: {
    value: {
      type: Object,
      default: () => ({})
    },
  },
  mounted() {
    this.intlVal = Object.keys( this.value ).map( x => ({
      data: {
        key: x,
        value: this.value[x]
      }
    }))
  },
  data() {
    return {
      intlVal: [],
      collapse: false,
    }
  },
  methods: {
    input() {
      this.$emit( 'input', this.objectVal );
      this.$emit( 'change', this.objectVal );
    },
    addTuple() {
      this.intlVal.push({ data: { key: '', value: null }});
    }
  },
  computed: {
    objectVal() {
      var o = {}
      this.intlVal.forEach( x => {
        o[x.key] = x.value
      });
      return o
    }
  }
}
</script>

<style lang="scss">
.json-object {
}
</style>
