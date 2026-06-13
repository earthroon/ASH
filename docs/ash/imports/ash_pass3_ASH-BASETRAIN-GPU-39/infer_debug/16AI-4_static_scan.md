# 16AI-4 Static Scan

## Patched symbols
803:        self.manifest.special_tokens.unk.id
810:    fn exact_core_special_id(&self, text: &str) -> Option<u32> {
811:        let specials = &self.manifest.special_tokens;
865:            .exact_core_special_id(text)
866:            .or_else(|| self.exact_core_special_id(&normalized))
894:                .unwrap_or_else(|| self.manifest.special_tokens.unk.token.clone());

## Forbidden generation/native changes scan
