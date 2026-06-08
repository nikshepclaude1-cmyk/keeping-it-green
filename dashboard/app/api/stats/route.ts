import { NextResponse } from "next/server";

const GITHUB_USER = "nikshep254";
const GITHUB_REPO = "keeping-it-green";

export async function GET() {
  const token = process.env.GITHUB_TOKEN;

  // fetch stats.json
  const statsRes = await fetch(
    `https://api.github.com/repos/${GITHUB_USER}/${GITHUB_REPO}/contents/stats.json`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
        Accept: "application/vnd.github.raw+json",
      },
      next: { revalidate: 300 },
    }
  );

  // fetch recent commits
  const commitsRes = await fetch(
    `https://api.github.com/repos/${GITHUB_USER}/${GITHUB_REPO}/commits?per_page=20`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
        Accept: "application/vnd.github+json",
      },
      next: { revalidate: 300 },
    }
  );

  const stats = statsRes.ok ? await statsRes.json() : null;
  const commits = commitsRes.ok ? await commitsRes.json() : [];

  return NextResponse.json({ stats, commits });
}
