depends = ('ITKPyBase', 'ITKImageGrid', 'ITKIOImageBase', 'ITKCommon', )
templates = (
  ('FixedPointInverseDisplacementFieldImageFilter', 'itk::FixedPointInverseDisplacementFieldImageFilter', 'itkFixedPointInverseDisplacementFieldImageFilterIVF22IVF22', True, 'itk::Image< itk::Vector< float,2 >,2 >, itk::Image< itk::Vector< float,2 >,2 >'),
  ('FixedPointInverseDisplacementFieldImageFilter', 'itk::FixedPointInverseDisplacementFieldImageFilter', 'itkFixedPointInverseDisplacementFieldImageFilterIVF33IVF33', True, 'itk::Image< itk::Vector< float,3 >,3 >, itk::Image< itk::Vector< float,3 >,3 >'),
)
snake_case_functions = ('fixed_point_inverse_displacement_field_image_filter', )
