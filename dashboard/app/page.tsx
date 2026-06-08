async function getStats(): Promise<Stats> {
  try {
    const res = await fetch(`${process.env.NEXT_PUBLIC_BASE_URL || ""}/api/stats`, {
      next: { revalidate: 300 },
    });
    if (!res.ok) throw new Error();
    const { stats } = await res.json();
    return stats ?? { total_commits: 0, streak_days: 0, today_commits: 0, last_updated: null, recent: [] };
  } catch {
    return { total_commits: 0, streak_days: 0, today_commits: 0, last_updated: null, recent: [] };
  }
}

async function getGitHubCommits() {
  try {
    const res = await fetch(`${process.env.NEXT_PUBLIC_BASE_URL || ""}/api/stats`, {
      next: { revalidate: 300 },
    });
    if (!res.ok) return [];
    const { commits } = await res.json();
    return commits as { sha: string; commit: { message: string; author: { date: string } } }[];
  } catch {
    return [];
  }
}
