<template lang="html">
  <span class="json-object">
    <span class="json-delim">{</span>
    <vk-btn v-if="intlVal.length > 1" class="json-collapse" type="light"
            @click.prevent="collapse=!collapse">
      <font-awesome-icon :icon="collapse ? 'plus' : 'minus' " />
    </vk-btn>
    <span v-if="collapse" class="json-object-content">...</span>
    <span v-else :class="[ 'json-object-content', intlVal.length > 1 ? '' : 'single' ]">
      <template v-for="v in intlVal">
        <json-tuple :readonly="readonly" :key="v.data.key" v-model="v.data"
                    :edit="v.edit"
                    @input="input" />
      </template>
    </span>
    <vk-btn v-if="editing && !collapse" class="json-add" type="light"
            @click.prevent="addTuple">
      <font-awesome-icon icon="plus" />
    </vk-btn>
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
  components: {
    VkBtn,
    JsonTuple,
    FontAwesomeIcon,
  },
  props: {
    value: {
      type: Object,
      default: () => ({})
    },
  },
  mounted() {
  },
  data() {
    return {
      intlVal: [],
      collapse: false,
    }
  },
  methods: {
    initVal() {
      this.intlVal = Object.keys( this.value ).map( x => ({
        data: {
          key: x,
          value: this.value[x]
        }
      }));
    },
    input() {
      this.$emit( 'input', this.objectVal );
    },
    addTuple() {
      this.intlVal.push({ data: { key: '', value: null },
                          edit: true });
    }
  },
  computed: {
    objectVal() {
      var o = {}
      this.intlVal.forEach( x => {
        o[x.data.key] = x.data.value
      });
      return o
    }
  },
  watch: {
    value( val ) {
      this.initVal();
    }
  }
}
</script>

<style lang="scss">
.json-object {
  .json-object-content.single .json-tuple {
    display: inline;
  }
}
</style>
