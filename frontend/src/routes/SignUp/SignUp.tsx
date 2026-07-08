import { useForm } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';

import { useAuth } from '@/contexts/AuthContext/AuthContext';
import { BASE_URL } from '@/utils/constants';

interface FormValues {
  username: string;
  email: string;
  password: string;
}

const SignUp = () => {
  const { login } = useAuth();
  const navigate = useNavigate();

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<FormValues>();

  const onSubmit = async (data: FormValues) => {
    try {
      const res = await fetch(`${BASE_URL}/auth/signup`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });

      const json = await res.json();

      if (!res.ok) {
        toast.error(json.detail ?? 'Sign up failed.');
        return;
      }

      login(json.access_token, json.refresh_token);
      toast.success('Account created! Welcome.');
      navigate('/todos');
    } catch {
      toast.error('Unable to reach the server. Please try again.');
    }
  };

  const inputClass =
    'w-full px-3 py-2.5 border border-[#ccc] rounded-md text-base font-[inherit] outline-none transition-[border-color,box-shadow] duration-200 hover:border-[#aaa] focus:border-[#2a9d8f] focus:shadow-[0_0_0_3px_rgba(42,157,143,0.2)]';

  const fieldClass = 'flex flex-col gap-1';

  return (
    <section>
      <h1>Sign Up</h1>
      <form className="flex flex-col gap-3 max-w-[360px]" onSubmit={handleSubmit(onSubmit)}>
        <div className={fieldClass}>
          <label htmlFor="username" className="text-sm font-medium">Username</label>
          <input
            id="username"
            type="text"
            className={inputClass}
            {...register('username', {
              required: 'Username is required.',
              minLength: { value: 3, message: 'Username must be at least 3 characters.' },
            })}
          />
          {errors.username && (
            <p className="flex items-center gap-1 text-[#c0392b] text-[0.85rem] before:content-['⚠'] before:text-[0.9rem] m-0">
              {errors.username.message}
            </p>
          )}
        </div>

        <div className={fieldClass}>
          <label htmlFor="email" className="text-sm font-medium">Email</label>
          <input
            id="email"
            type="email"
            className={inputClass}
            {...register('email', {
              required: 'Email is required.',
              pattern: {
                value: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
                message: 'Enter a valid email address.',
              },
            })}
          />
          {errors.email && (
            <p className="flex items-center gap-1 text-[#c0392b] text-[0.85rem] before:content-['⚠'] before:text-[0.9rem] m-0">
              {errors.email.message}
            </p>
          )}
        </div>

        <div className={fieldClass}>
          <label htmlFor="password" className="text-sm font-medium">Password</label>
          <input
            id="password"
            type="password"
            className={inputClass}
            {...register('password', {
              required: 'Password is required.',
              minLength: { value: 8, message: 'Password must be at least 8 characters.' },
            })}
          />
          {errors.password && (
            <p className="flex items-center gap-1 text-[#c0392b] text-[0.85rem] before:content-['⚠'] before:text-[0.9rem] m-0">
              {errors.password.message}
            </p>
          )}
        </div>

        <button
          type="submit"
          disabled={isSubmitting}
          className="self-start mt-1 px-6 py-3 bg-[#2a9d8f] hover:bg-[#21867a] hover:-translate-y-px text-white border-none rounded-md text-base font-[inherit] cursor-pointer transition-[background-color,transform] duration-200 disabled:opacity-60 disabled:cursor-not-allowed disabled:transform-none"
        >
          {isSubmitting ? 'Creating account...' : 'Sign Up'}
        </button>
      </form>
    </section>
  );
};

export default SignUp;
