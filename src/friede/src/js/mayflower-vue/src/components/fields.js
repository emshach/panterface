const BooleanField = () =>
        import(/* webpackChunkName: "fields" */ '@/components/wx/f/BooleanField' )
const CharField = () =>
        import(/* webpackChunkName: "fields" */ '@/components/wx/f/CharField' )
const TextField = () =>
        import(/* webpackChunkName: "fields" */ '@/components/wx/f/TextField' )
const JsonField = () =>
        import(/* webpackChunkName: "fields" */ '@/components/wx/f/JSONField' )
const ChoiceField = () =>
        import(/* webpackChunkName: "fields" */ '@/components/wx/f/ChoiceField' )
const TypedChoiceField = () =>
        import(/* webpackChunkName: "fields" */ '@/components/wx/f/TypedChoiceField' )
const DateField = () =>
        import(/* webpackChunkName: "fields" */ '@/components/wx/f/DateField' )
const DateTimeField = () =>
        import(/* webpackChunkName: "fields" */ '@/components/wx/f/DateTimeField' )
const DecimalField = () =>
        import(/* webpackChunkName: "fields" */ '@/components/wx/f/DecimalField' )
const DurationField = () =>
        import(/* webpackChunkName: "fields" */ '@/components/wx/f/DurationField' )
const EmailField = () =>
        import(/* webpackChunkName: "fields" */ '@/components/wx/f/EmailField' )
const FileField = () =>
        import(/* webpackChunkName: "fields" */ '@/components/wx/f/FileField' )
const FilePathField = () =>
        import(/* webpackChunkName: "fields" */ '@/components/wx/f/FilePathField' )
const FloatField = () =>
        import(/* webpackChunkName: "fields" */ '@/components/wx/f/FloatField' )
const ImageField = () =>
        import(/* webpackChunkName: "fields" */ '@/components/wx/f/ImageField' )
const IntegerField = () =>
        import(/* webpackChunkName: "fields" */ '@/components/wx/f/IntegerField' )
const IpAddressField = () =>
        import(/* webpackChunkName: "fields" */ '@/components/wx/f/IPAddressField' )
const MultipleChoiceField = () =>
const GenericIpAddressField = () =>
        import(/* webpackChunkName: "fields" */ '@/components/wx/f/GenericIPAddressField' )
        import(/* webpackChunkName: "fields" */ '@/components/wx/f/MultipleChoiceField' )
const TypedMultipleChoiceField = () =>
        import(/* webpackChunkName: "fields" */ '@/components/wx/f/TypedMultipleChoiceField' )
const NullBooleanField = () =>
        import(/* webpackChunkName: "fields" */ '@/components/wx/f/NullBooleanField' )
const RegexField = () =>
        import(/* webpackChunkName: "fields" */ '@/components/wx/f/RegexField' )
const SlugField = () =>
        import(/* webpackChunkName: "fields" */ '@/components/wx/f/SlugField' )
const TimeField = () =>
        import(/* webpackChunkName: "fields" */ '@/components/wx/f/TimeField' )
const UrlField = () =>
        import(/* webpackChunkName: "fields" */ '@/components/wx/f/URLField' )
const UuidField = () =>
        import(/* webpackChunkName: "fields" */ '@/components/wx/f/UUIDField' )
// const ComboField = () =>
//         import(/* webpackChunkName: "fields" */ '@/components/wx/f/ComboField' )
const MultiValueField = () =>
        import(/* webpackChunkName: "fields" */ '@/components/wx/f/MultiValueField' )
const SplitDateTimeField = () =>
        import(/* webpackChunkName: "fields" */ '@/components/wx/f/SplitDateTimeField' )
const ModelChoiceField = () =>
        import(/* webpackChunkName: "fields" */ '@/components/wx/f/ModelChoiceField' )
const ModelMultipleChoiceField = () =>
        import(/* webpackChunkName: "fields" */ '@/components/wx/f/ModelMultipleChoiceField' )

const ChoicesField = MultipleChoiceField;
const TypedChoicesField = TypedMultipleChoiceField;
const ModelField = ModelChoiceField;
const ModelsField = ModelMultipleChoiceField;

export {
  BooleanField,
  CharField,
  TextField,
  JsonField,
  ChoiceField,
  TypedChoiceField,
  DateField,
  DateTimeField,
  DecimalField,
  DurationField,
  EmailField,
  FileField,
  FilePathField,
  FloatField,
  ImageField,
  IntegerField,
  IpAddressField,
  GenericIpAddressField,
  MultipleChoiceField,
  TypedMultipleChoiceField,
  NullBooleanField,
  RegexField,
  SlugField,
  TimeField,
  UrlField,
  UuidField,
  ComboField,
  MultiValueField,
  SplitDateTimeField,
  ModelChoiceField,
  ModelMultipleChoiceField,
  // shortcuts
  ChoicesField,
  TypedChoicesField,
  ModelField,
  ModelsField
}
export default {
  BooleanField,
  CharField,
  TextField,
  JsonField,
  ChoiceField,
  TypedChoiceField,
  DateField,
  DateTimeField,
  DecimalField,
  DurationField,
  EmailField,
  FileField,
  FilePathField,
  FloatField,
  ImageField,
  IntegerField,
  IpAddressField,
  GenericIpAddressField,
  MultipleChoiceField,
  TypedMultipleChoiceField,
  NullBooleanField,
  RegexField,
  SlugField,
  TimeField,
  UrlField,
  UuidField,
  ComboField,
  MultiValueField,
  SplitDateTimeField,
  ModelChoiceField,
  ModelMultipleChoiceField,
  // shortcuts
  IpAddressField,
  ChoicesField,
  TypedChoicesField,
  ModelField,
  ModelsField
}
