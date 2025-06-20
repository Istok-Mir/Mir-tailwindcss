from Mir import LanguageServer, LoaderInStatusBar, deno, PackageStorage, command


server_storage = PackageStorage(tag='0.0.1', sync_folder="./language-server")


class TailwindcssLanguageServer(LanguageServer):
    name='tailwindcss'
    activation_events={
        'selector': 'source.jsx | source.js.react | source.js | source.tsx | source.ts | source.css | source.scss | source.less | text.html.vue | text.html.svelte | text.html.basic | text.html.twig | text.blade | text.html.blade | embedding.php | text.html.rails | text.html.erb | text.haml | text.jinja | text.django | text.html.elixir | source.elixir | text.html.ngx | source.astro',
        'workspace_contains': ['**/tailwind.config.{ts,js,cjs,mjs}'],
    }
    settings_file="Mir-tailwindcss.sublime-settings"

    async def activate(self):
        # setup runtime and install dependencies
        await deno.setup()
        server_path = server_storage / "language-server" / "node_modules" / "@tailwindcss" / "language-server" / "bin" / "tailwindcss-language-server"
        if not server_path.exists():
            with LoaderInStatusBar(f'installing {self.name}'):
                await command([deno.path, "install"], cwd=str(server_storage / "language-server"))

        await self.connect('stdio', {
            'cmd': [deno.path, 'run', '-A', server_path, '--stdio'],
        })

