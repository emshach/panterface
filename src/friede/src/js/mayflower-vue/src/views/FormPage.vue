<template lang="html">
  <div :class=classes >
    <vk-card :class="[ 'form-page', scrolled ]" >
      <div slot="header">
        <div class="form-controls uk-align-right uk-text-right">
          <vk-btn type="text" @click.prevent="settings">
            <font-awesome-icon icon="cog" />
          </vk-btn>
          <vk-btn type="text" @click.prevent="discard">
            <font-awesome-icon icon="trash" /> discard
          </vk-btn>
          <vk-btn-grp>
            <vk-btn v-if="editList.length && editing" type="primary"
                    @click.prevent="prev">
              <vk-icon-left />
            </vk-btn>
            <vk-btn type="primary" @click.prevent="submit">
              <font-awesome-icon icon="check" /> done
            </vk-btn>
            <vk-btn v-if="mode==='new'" type="primary" @click.prevent="submitAndRedo">
              <font-awesome-icon icon="plus" /> and another
            </vk-btn>
            <vk-btn v-else-if="editList.length && editing < editList.length - 1 "
                    type="primary" @click.prevent="next">
              <vk-icon-right />
            </vk-btn>
          </vk-btn-grp>
        </div>
        <vk-card-title class="uk-align-left">{{ location.title }}</vk-card-title>
      </div>
      <vue-perfect-scrollbar class="scroller" slot="body"
                             @ps-scroll-down="scrolled='scrolled'"
                             @ps-y-reach-start="scrolled=''">
        <form v-if="model" class="uk-form-horizontal uk-text-left">
          <input v-for="field in readOnlyFields" type="hidden" :value=field.value />
          <field v-for="field in simpleFields" :key=field.meta.name
                 :type=field.meta.type :name=field.meta.name :data=field
                 class="uk-margin" />
          <field v-for="field in complexFields" :key=field.meta.name
                 :type=field.meta.type :name=field.meta.name :data=field
                 :fieldset=true />
      </form>
      </vue-perfect-scrollbar>
    </vk-card>
  </div>
</template>

<script lang="js">
import { Card as VkCard, CardTitle as VkCardTitle } from 'vuikit/lib/card'
import { Button as VkBtn, ButtonGroup as VkBtnGrp } from 'vuikit/lib/button'
import {
  IconChevronLeft as VkIconLeft,
  IconChevronRight as VkIconRight
} from '@vuikit/icons'
import { faCheck, faPlus, faTrash, faCog } from '@fortawesome/free-solid-svg-icons'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { Field } from '@/components'
import { Model } from '@/lib/objects'
import { PageMixin } from '@/lib/mixins'

library.add( faCheck, faPlus, faTrash, faCog )

export default  {
  name: 'FormPage',
  mixins: [ PageMixin ],
  components: {
    VkCard,
    VkCardTitle,
    VkBtn,
    VkBtnGrp,
    VkIconLeft,
    VkIconRight,
    Field
  },
  props: {
    mode: {
      type: String,
      default: 'new'
    },
    editList: {
      type: Array,
      default: () => []
    },
    editing: {
      type: Number,
      default: 0
    }
  },
  mounted() {
  },
  data() {
    return {
      data: null,
      scrolled: ''
    }
  },
  methods: {
    settings() {
    },
    submit() {
    },
    submitAndRedo() {
      this.$router.push('');
    },
    discard() {
    },
    prev() {
      this.submit();
      if ( this.editing )
        this.editing--;
    },
    next() {
      this.submit();
      if ( this.editing < this.editList - 1 )
        this.editing++;
    }
  },
  computed: {
    modelData() {
      if ( this.data )
        return this.data;
      if ( this.$store.state.modelData )
        this.data = this.$store.state.modelData;
      else if ( this.model ) {
        const id = this.objectId;
        if ( typeof this.model === 'string' ) {
          if ( this.$store.state.models[ this.model ])
            ( this.data = Model( Object.assign(
              { id }, this.$store.state.models[ this.model ] )))
             .ready.then( r => {
               if ( !id && this.data.data.id )
                 this.$router.replace( `?id=${this.data.data.id}` );
             });
        } else
          ( this.data = Model( Object.assign( { id }, this.model )))
           .ready.then( r => {
             if ( !id && this.data.data.id )
               this.$router.replace( `?id=${this.data.data.id}` );
           });
      }
      if ( this.data && this.data.data && this.data.data.id )
        this.$router.replace( `?id=${this.data.data.id}` );
      return this.data || Model({ fields: [] });
    },
    objectId() {
      return this.$route.query && this.$route.query.id;
    }, 
    location() {
      return this.$store.state.location
    },
    readOnlyFields() {
      return this.modelData.fields.filter(
        x => !x.meta.related || x.meta.type.match( /ReadOnly/ ));
    },
    simpleFields() {
      return this.modelData.fields.filter(
        x => !x.meta.related || !x.meta.type.match( /Multiple|Choices|ReadOnly/ ));
    },
    complexFields() {
      return this.modelData.fields.filter(
        x => x.meta.related && x.meta.type.match( /Multiple|Choices|ReadOnly/ ));
    },
  },
  watch: {
    'modelData.data.id'() {
      if ( this.modelData && this.modelData.data && this.modelData.data.id )
        this.$router.replace( `?id=${this.modelData.data.id}` );
    },
    objectId( val ) {
      if ( this.data && this.data.data.id && val !== this.data.data.id )
        this.data = null;
    },
    model() {
      this.$nextTick(() => this.getData().then(() => {
        this.data = null;
      }));
    },
  }
}
</script>

<style lang="scss">
.form-page {
  border-radius: 2px;
  height: 100%;
  flex: 1;
  > .uk-card-header {
    padding: 0;
    border-bottom: none;
    .uk-card-title{
      margin: 6px 14px;
    }
    .form-controls{
      margin-bottom: 0;
    }
    .uk-button {
      font-size: 0.95rem;
      line-height: 34px;
      padding: 0 12px;
    }
    .uk-button-group {
      .uk-button:first-child {
        /* border-top-left-radius: 2px; */
        border-bottom-left-radius: 2px;
      }
      .uk-button:last-child {
        border-top-right-radius: 2px;
        /* border-bottom-right-radius: 2px; */
      }
    }
  }
  .uk-card-body {
    height: calc( 100% - 45px );
    box-sizing: border-box;
    padding: 6px 0px 1px 24px;
    > .scroller {
      height: 100%;
      padding-right: 16px;
    }
  }
  &.scrolled .uk-card-body {
    box-shadow: inset 0 12px 11px -11px rgba(0, 0, 0, 0.1);
  }
  .no-data {
    color: rgba(0,0,0,0.35);
  }
  .btn-confirm {
    color: limegreen;
    &:hover {
      color: forestgreen;
    }
  }
  .btn-cancel {
    color: red;
    &:hover {
      color: darkred;
    }
  }
}
</style>
