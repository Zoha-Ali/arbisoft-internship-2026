import { useForm } from 'react-hook-form';
import { Link, useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';

import { useAuth } from '@/contexts/AuthContext/AuthContext';
import { BASE_URL } from '@/utils/constants';

interface FormValues {
  email: string;
  password: string;
}

const SignIn = () => {
  const { login } = useAuth();
  const navigate = useNavigate();

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<FormValues>();

  const onSubmit = async (data: FormValues) => {
    try {
      const res = await fetch(`${BASE_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });

      const json = await res.json();

      if (!res.ok) {
        toast.error(json.detail ?? 'Sign in failed.');
        return;
      }

      login(json.access_token, json.refresh_token);
      toast.success('Welcome back!');
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
      <h1>Sign In</h1>
      <form className="flex flex-col gap-3 max-w-[360px]" onSubmit={handleSubmit(onSubmit)}>
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
          {isSubmitting ? 'Signing in...' : 'Sign In'}
        </button>

        <p className="text-sm text-[#555] m-0">
          Don't have an account?{' '}
          <Link to="/signup" className="text-[#2a9d8f] hover:underline">Sign up</Link>
        </p>
      </form>
    </section>
  );
};

export default SignIn;
