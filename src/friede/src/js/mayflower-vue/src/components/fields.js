export const BooleanField = () =>
      import(/* webpackChunkName: "fields" */ '@/components/wx/f/BooleanField' )
export const CharField = () =>
      import(/* webpackChunkName: "fields" */ '@/components/wx/f/CharField' )
export const TextField = () =>
      import(/* webpackChunkName: "fields" */ '@/components/wx/f/TextField' )
export const JsonField = () =>
      import(/* webpackChunkName: "fields" */ '@/components/wx/f/JSONField' )
export const ChoiceField = () =>
      import(/* webpackChunkName: "fields" */ '@/components/wx/f/ChoiceField' )
export const TypedChoiceField = () =>
      import(/* webpackChunkName: "fields" */ '@/components/wx/f/TypedChoiceField' )
export const DateField = () =>
      import(/* webpackChunkName: "fields" */ '@/components/wx/f/DateField' )
export const DateTimeField = () =>
      import(/* webpackChunkName: "fields" */ '@/components/wx/f/DateTimeField' )
export const DecimalField = () =>
      import(/* webpackChunkName: "fields" */ '@/components/wx/f/DecimalField' )
export const DurationField = () =>
      import(/* webpackChunkName: "fields" */ '@/components/wx/f/DurationField' )
export const EmailField = () =>
      import(/* webpackChunkName: "fields" */ '@/components/wx/f/EmailField' )
export const FileField = () =>
      import(/* webpackChunkName: "fields" */ '@/components/wx/f/FileField' )
export const FilePathField = () =>
      import(/* webpackChunkName: "fields" */ '@/components/wx/f/FilePathField' )
export const FloatField = () =>
      import(/* webpackChunkName: "fields" */ '@/components/wx/f/FloatField' )
export const ImageField = () =>
      import(/* webpackChunkName: "fields" */ '@/components/wx/f/ImageField' )
export const IntegerField = () =>
      import(/* webpackChunkName: "fields" */ '@/components/wx/f/IntegerField' )
export const IpAddressField = () =>
      import(/* webpackChunkName: "fields" */ '@/components/wx/f/IPAddressField' )
export const MultipleChoiceField = () =>
      import(/* webpackChunkName: "fields" */ '@/components/wx/f/MultipleChoiceField' )
export const GenericIpAddressField = () =>
      import(/* webpackChunkName: "fields" */ '@/components/wx/f/GenericIPAddressField' )
export const TypedMultipleChoiceField = () =>
      import(/* webpackChunkName: "fields" */ '@/components/wx/f/TypedMultipleChoiceField' )
export const NullBooleanField = () =>
      import(/* webpackChunkName: "fields" */ '@/components/wx/f/NullBooleanField' )
export const RegexField = () =>
      import(/* webpackChunkName: "fields" */ '@/components/wx/f/RegexField' )
export const SlugField = () =>
      import(/* webpackChunkName: "fields" */ '@/components/wx/f/SlugField' )
export const TimeField = () =>
      import(/* webpackChunkName: "fields" */ '@/components/wx/f/TimeField' )
export const UrlField = () =>
      import(/* webpackChunkName: "fields" */ '@/components/wx/f/URLField' )
export const UuidField = () =>
      import(/* webpackChunkName: "fields" */ '@/components/wx/f/UUIDField' )
export const ComboField = () =>
      import(/* webpackChunkName: "fields" */ '@/components/wx/f/ComboField' )
export const MultiValueField = () =>
      import(/* webpackChunkName: "fields" */ '@/components/wx/f/MultiValueField' )
export const SplitDateTimeField = () =>
      import(/* webpackChunkName: "fields" */ '@/components/wx/f/SplitDateTimeField' )
export const ModelChoiceField = () =>
      import(/* webpackChunkName: "fields" */ '@/components/wx/f/ModelChoiceField' )
export const ModelMultipleChoiceField = () =>
      import(/* webpackChunkName: "fields" */ '@/components/wx/f/ModelMultipleChoiceField' )

export const ChoicesField = MultipleChoiceField;
export const TypedChoicesField = TypedMultipleChoiceField;
export const ModelField = ModelChoiceField;
export const ModelsField = ModelMultipleChoiceField;

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
