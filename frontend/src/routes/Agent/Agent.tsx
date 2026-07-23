import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';

import { useAuth } from '@/contexts/AuthContext/AuthContext';
import { BASE_URL } from '@/utils/constants';

interface TraceEntry {
  ts: string;
  agent: string;
  event: string;
}

const AGENT_COLORS: Record<string, string> = {
  supervisor:       'text-[#e76f51]',
  research_worker:  'text-[#2a9d8f]',
  todo_worker:      'text-[#457b9d]',
};

const Agent = () => {
  const { accessToken, isLoading } = useAuth();
  const navigate = useNavigate();

  const [question, setQuestion]     = useState('');
  const [answer, setAnswer]         = useState('');
  const [trace, setTrace]           = useState<TraceEntry[]>([]);
  const [traceOpen, setTraceOpen]   = useState(false);
  const [loading, setLoading]       = useState(false);

  const inputClass =
    'w-full px-3 py-2.5 border border-[#ccc] rounded-md text-base font-[inherit] outline-none transition-[border-color,box-shadow] duration-200 hover:border-[#aaa] focus:border-[#2a9d8f] focus:shadow-[0_0_0_3px_rgba(42,157,143,0.2)]';

  // Show a loading placeholder while the auth state is being restored from
  // localStorage — prevents a flash of the "sign in" prompt for logged-in users.
  if (isLoading) return <p>Loading...</p>;

  // Gate the page: unauthenticated users see a prompt instead of the form.
  if (!accessToken) {
    return (
      <section>
        <h1>Ask the Agent</h1>
        <p className="text-[#555]">
          You need to be signed in to use the agent.{' '}
          <Link to="/signin" className="text-[#2a9d8f] hover:underline">Sign in</Link>
        </p>
      </section>
    );
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim()) return;

    setLoading(true);
    setAnswer('');
    setTrace([]);
    setTraceOpen(false);

    try {
      const res = await fetch(`${BASE_URL}/orchestrator/ask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${accessToken}`,
        },
        body: JSON.stringify({ question }),
      });

      const json = await res.json();

      if (!res.ok) {
        if (res.status === 401) {
          toast.error('Session expired. Please sign in again.');
          navigate('/signin');
          return;
        }
        toast.error(json.detail ?? 'Agent request failed.');
        return;
      }

      setAnswer(json.answer);
      setTrace(json.trace ?? []);
    } catch {
      toast.error('Unable to reach the server. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <section>
      <h1>Ask the Agent</h1>
      <form className="flex flex-col gap-3 max-w-[560px]" onSubmit={handleSubmit}>
        <div className="flex flex-col gap-1">
          <label htmlFor="question" className="text-sm font-medium">Your question</label>
          <textarea
            id="question"
            rows={3}
            className={`${inputClass} resize-y`}
            placeholder="e.g. What is the latest version of Python?"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            disabled={loading}
          />
        </div>

        <button
          type="submit"
          disabled={loading || !question.trim()}
          className="self-start mt-1 px-6 py-3 bg-[#2a9d8f] hover:bg-[#21867a] hover:-translate-y-px text-white border-none rounded-md text-base font-[inherit] cursor-pointer transition-[background-color,transform] duration-200 disabled:opacity-60 disabled:cursor-not-allowed disabled:transform-none"
        >
          {loading ? 'Thinking...' : 'Ask'}
        </button>
      </form>

      {answer && (
        <div className="mt-6 max-w-[560px] flex flex-col gap-3">
          <div className="p-4 border border-[#2a9d8f] rounded-md bg-[rgba(42,157,143,0.06)]">
            <p className="text-sm font-medium text-[#2a9d8f] mb-2">Answer</p>
            <p className="text-base whitespace-pre-wrap m-0">{answer}</p>
          </div>

          {trace.length > 0 && (
            <div className="border border-[#ddd] rounded-md overflow-hidden">
              <button
                type="button"
                onClick={() => setTraceOpen((o) => !o)}
                className="w-full flex items-center justify-between px-4 py-2.5 bg-[#f7f7f7] text-sm font-medium text-[#555] hover:bg-[#eee] transition-colors duration-150 cursor-pointer border-none"
              >
                <span>Agent trace ({trace.length} steps)</span>
                <span className="text-xs text-[#999]">{traceOpen ? '▲ hide' : '▼ show'}</span>
              </button>

              {traceOpen && (
                <ol className="m-0 p-0 list-none divide-y divide-[#eee]">
                  {trace.map((entry, i) => (
                    <li key={i} className="flex gap-3 px-4 py-2 text-sm font-mono">
                      <span className="shrink-0 text-[#aaa]">{entry.ts}</span>
                      <span className={`shrink-0 w-[140px] font-semibold ${AGENT_COLORS[entry.agent] ?? 'text-[#333]'}`}>
                        {entry.agent}
                      </span>
                      <span className="text-[#444] break-all">{entry.event}</span>
                    </li>
                  ))}
                </ol>
              )}
            </div>
          )}
        </div>
      )}
    </section>
  );
};

export default Agent;
