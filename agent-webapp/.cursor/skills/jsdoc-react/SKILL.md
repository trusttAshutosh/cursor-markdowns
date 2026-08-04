---
name: jsdoc-react
description: Add JSDoc block comments to React helpers, hooks, interceptors, api, context, and common components following project standards. Use when the user asks for JSDoc, documentation, or documenting new/modified exported functions, hooks, or components.
---

# JSDoc for React (Project Standard)

## When to use

- User asks to add JSDoc, run a documentation pass, or review for missing docs
- You are creating or modifying exported symbols in scoped infrastructure or common-component files

## Workflow

1. Read the target file and identify exported/public symbols
2. Check which rule applies:
   - **Strict**: `src/helpers/**`, `src/hooks/**`, `src/Config/customHooks/**`, `src/**/hooks/**`, `src/Config/axios/requestInterceptor/**`, `src/api/**`, `src/context/**`
   - **Warn**: `src/components/common/**`
3. Add docs only on **new or modified** symbols — do not backfill untouched exports
4. Skip trivial re-exports in barrel `index.ts`; document at the definition site
5. Skip trivial one-liners where name + types are self-explanatory

## React-specific guidance

- **Components**: prefer prop-level JSDoc on exported props interfaces over `@param` on the component when props are a single object
- **Hooks**: document the hook summary and return shape (`@returns`); do not document every internal `useSelector` / `useState`
- **Context**: one-line summary on the provider; document non-obvious fields on the context value interface if exported
- **Interceptors**: summary + `@param` for the request/config when behavior is non-obvious
- **Helpers**: `@param` per non-obvious argument; `@returns` when returning a value

## Comment format

```typescript
/**
 * One-sentence summary of what this symbol does.
 * @param name - Description when non-obvious.
 * @returns Description of return value when applicable.
 */
```

Use `/** */` only — not `//` line comments for public API docs.

## Checklist

- [ ] Every new/modified exported function, hook, provider, or component has a summary
- [ ] Hooks and functions that return values include `@returns`
- [ ] Non-obvious parameters have `@param`
- [ ] No docs added to unchanged legacy exports
- [ ] No duplicate docs on re-export barrels

## Examples

See [examples.md](examples.md) for repo-aligned helper, hook, context, interceptor, component, and **TypeScript** before/after patterns.
