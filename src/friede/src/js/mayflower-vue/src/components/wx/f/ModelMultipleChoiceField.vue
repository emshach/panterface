<template lang="html">
  <div class="model-multiple-choice-field" >
    <vk-table v-if="isset" :data="field.value||[]">
      <vk-table-column v-for="c in columns"
                       :key="c.name" :title="c.name" :name="c.name" />
    </vk-table>
    <div v-else v-html="html" @click="editField" @focus="editField"
         :class="fieldClasses" />
    <div :class="fieldClasses">
      <template v-if="editMode">
        <label>
          add
          <vk-button-link class="btn btn-confirm" @click.prevent="commit">
            <font-awesome-icon icon="check" /> done
          </vk-button-link>
          <vk-button-link class="btn btn-cancel" @click.prevent="cancel">
            <font-awesome-icon icon="times" /> cancel
          </vk-button-link>
          <multiselect v-model="values" ref="inputV"
                       :options="options"
                       :multiple="true"
                       label="title"
                       track-by="path"
                       open-direction="bottom"
                       @search-change="getObjects"
                       />
        </label>
      </template>
      <vk-button-link v-else @click="editField" @focus="editField">
        add
      </vk-button-link>
    </div>
  </div>
</template>

<script lang="js">
import { Field } from '@/lib/objects'
import { Table as VkTable, TableColumn as VkTableColumn } from 'vuikit/lib/table'
import { ButtonLink as VkButtonLink } from 'vuikit/lib/button'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faTimes, faCheck } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { ModelFieldMixin, ModelModelsFieldMixin } from '@/lib/mixins'

library.add( faTimes, faCheck )

export default {
  name: 'ModelMultipleChoiceField',
  mixins: [ ModelFieldMixin, ModelModelsFieldMixin ],
  components: {
    VkTable,
    VkTableColumn,
    VkButtonLink,
    FontAwesomeIcon,
  },
  props: {},
  mounted() {
    const m = this.field.meta.related;
    this.related = this.$store.state.models[m];
  },
  data() {
    return {
      related: null,
    }
  },
  methods: {
    commit() {
      const m = this.field.meta.related;
      let l = this.field.meta.link_field;
      if ( !l ) {
        this.commitField();
        return;
      }
      if ( this.values.length ) {
        const model = this.$store.state.models[m];
        var values = this.values.map( v => {
          var link = { _model: model };
          model.fields.forEach( f => {
            link[ f.name ] = Field(f).value;
          });
          link[l] = v;
          return link;
        });
        this.field.wip = ( this.field.wip || [] ).concat( values );
        this.values = [];
        return;
      }
      this.commitField();
    },
    cancel() {
      if ( this.values.length ) {
          this.values = [];
        return;
      }
      this.revertField();
    }
  },
  computed: {
    columns() {
      return this.related ? this.related.fields : [];
    },
    searchModel() {
      let l = this.field.meta.link_field;
      if (l) {
        const model = this.related;
        var f = model && model.fields.find( x => x.name === l );
        return f && f.related;
      }
      return this.field.meta.related;
    }
  }
}
</script>

<style scoped lang="scss">
.model-multiple-choice-field {
  .btn {
    padding: 0 7px;
    height: 30px;
    line-height: 33px;
    &.btn-confirm {
      color: limegreen;
      &:hover {
        color: forestgreen;
      }
    }
    &.btn-cancel {
      color: red;
      &:hover {
        color: darkred;
      }
    }
  }
}
</style>
