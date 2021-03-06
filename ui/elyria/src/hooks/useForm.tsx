import { ChangeEvent, useEffect, useState } from 'react';

export default function useForm<T>(initial: T) {
  const [inputs, setInputs] = useState<T>(initial);
  const initialValues = Object.values(initial).join('');

  useEffect(() => {
    setInputs(initial);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [initialValues]);

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    let { value, name } = e.target;

    setInputs({
      ...inputs,
      [name]: value,
    });
  };

  const resetForm = () => {
    setInputs(initial);
  };

  const setValues = (values: T) => {
    setInputs(values);
  };

  return {
    inputs,
    handleChange,
    resetForm,
    setValues,
  };
}
