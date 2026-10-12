import { defineCollection } from 'astro:content';
import { z } from 'zod/v4';
import { glob } from 'astro/loaders';
const schema = z.object({
  title: z.string(),
  summary: z.string(),
  source: z.string(),
  order: z.number(),
  kind: z.string().optional(),
  date: z.string().optional(),
  image: z.string().optional(),
  alt: z.string().optional(),
  caption: z.string().optional(),
  imageKind: z.enum(['photo','diagram']).default('photo'),
  imagePlacement: z.enum(['all','detail']).default('all'),
  location: z.string().optional(),
  tags: z.array(z.string()).default([]),
  links: z.array(z.object({ label: z.string(), url: z.string() })).default([]),
  pending: z.array(z.string()).default([]),
  related: z.array(z.object({label:z.string(),url:z.string()})).default([]),
  reference: z.object({collection:z.string(),id:z.string()}).optional(),
  lidar: z.boolean().default(false)
});
const collection = (name: string) => defineCollection({ loader: glob({ pattern: '**/*.md', base: `./src/content/${name}` }), schema });
export const collections = {
  projects: collection('projects'), education: collection('education'), experience: collection('experience'),
  presentations: collection('presentations'), workshops: collection('workshops'), honors: collection('honors'),
  publications: collection('publications'), engagement: collection('engagement'), highlights: collection('highlights'),
  certifications: collection('certifications'), pages: collection('pages')
};
