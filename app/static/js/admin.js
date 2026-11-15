/* Кабинет кафедры: редактирование строк, фильтры, загрузка файлов, рапорт */
(function () {
  'use strict';
  const $ = (s, r) => (r || document).querySelector(s);
  const $$ = (s, r) => Array.from((r || document).querySelectorAll(s));

  // ---- Строки таблиц: изменить / удалить ----
  document.addEventListener('click', (e) => {
    const t = e.target.closest('button, a');
    if (!t) return;
    const row = t.closest('.tr');
    if (t.matches('[data-edit]') && row) {
      $$('.tr.is-editing, .tr.is-confirm').forEach((r) => { if (r !== row) r.classList.remove('is-editing', 'is-confirm'); });
      row.classList.add('is-editing');
      const first = $('.edit input, .edit select', row); if (first) first.focus();
    } else if (t.matches('[data-ask-delete]') && row) {
      $$('.tr.is-confirm').forEach((r) => r.classList.remove('is-confirm'));
      row.classList.add('is-confirm');
    } else if (t.matches('[data-cancel]') && row) {
      row.classList.remove('is-editing', 'is-confirm');
      if (row.tagName === 'FORM') row.reset();
      syncOwn(row);
    } else if (t.matches('[data-open]')) {
      const el = $(t.dataset.open); if (el) { el.classList.add('open'); const i = $('input', el); if (i) i.focus(); }
    } else if (t.matches('[data-close]')) {
      const el = $(t.dataset.close); if (el) { el.classList.remove('open'); el.reset && el.reset(); }
    } else if (t.matches('[data-copy], [data-copy-from]')) {
      const text = t.dataset.copy || ($(t.dataset.copyFrom) || {}).value || '';
      const done = () => { const old = t.textContent; t.textContent = t.dataset.copied || 'Скопировано'; setTimeout(() => { t.textContent = old; }, 2000); };
      if (navigator.clipboard && window.isSecureContext) navigator.clipboard.writeText(text).then(done);
      else { const ta = document.createElement('textarea'); ta.value = text; document.body.appendChild(ta); ta.select(); try { document.execCommand('copy'); done(); } catch (_) {} ta.remove(); }
    }
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') $$('.tr.is-editing, .tr.is-confirm').forEach((r) => r.classList.remove('is-editing', 'is-confirm'));
  });

  // ---- «Своё место практики»: показать поле названия ----
  function syncOwn(scope) {
    $$('select[data-own-toggle]', scope).forEach((sel) => {
      const title = sel.parentElement.querySelector('[data-own-title]');
      if (title) title.style.display = sel.value === 'Свое место практики' ? '' : 'none';
    });
  }
  document.addEventListener('change', (e) => { if (e.target.matches('select[data-own-toggle]')) syncOwn(e.target.parentElement); });

  // ---- Файлы: имя, автоотправка, перетаскивание ----
  document.addEventListener('change', (e) => {
    const input = e.target;
    if (input.type !== 'file') return;
    const label = input.closest('[data-drop]');
    const nameEl = label && $('[data-file-name]', label);
    if (nameEl) nameEl.textContent = Array.from(input.files).map((f) => f.name).join(', ');
    if (input.hasAttribute('data-autosubmit') && input.files.length) input.form.submit();
  });
  $$('[data-drop]').forEach((zone) => {
    const input = $('input[type=file]', zone);
    ['dragenter', 'dragover'].forEach((ev) => zone.addEventListener(ev, (e) => { e.preventDefault(); zone.classList.add('over'); }));
    ['dragleave', 'drop'].forEach((ev) => zone.addEventListener(ev, (e) => { e.preventDefault(); zone.classList.remove('over'); }));
    zone.addEventListener('drop', (e) => {
      if (!input || !e.dataTransfer.files.length) return;
      input.files = e.dataTransfer.files;
      input.dispatchEvent(new Event('change', { bubbles: true }));
    });
  });

  // ---- Фильтр студентов ----
  const bar = $('[data-filter-bar]');
  if (bar) {
    const table = $(bar.dataset.target);
    const search = $('[data-filter-search]', bar);
    const statusSel = $('[data-filter-status]', bar);
    const chips = $$('[data-filter-group]', bar);
    const shown = $('[data-shown]');
    const params = new URLSearchParams(location.search);
    let group = params.get('group') || '';
    if (params.get('status')) statusSel.value = params.get('status');
    const apply = () => {
      const q = search.value.trim().toLowerCase();
      const st = statusSel.value;
      let n = 0;
      chips.forEach((c) => c.setAttribute('aria-pressed', String(c.dataset.filterGroup === group)));
      $$('[data-row]', table).forEach((r) => {
        const ok = (!group || r.dataset.group === group)
          && (!q || r.dataset.search.indexOf(q) >= 0)
          && (!st || r.dataset.status === st);
        r.classList.toggle('hidden-row', !ok);
        if (ok) n++;
      });
      if (shown) shown.textContent = n;
    };
    chips.forEach((c) => c.addEventListener('click', () => { group = c.dataset.filterGroup; apply(); }));
    search.addEventListener('input', apply);
    statusSel.addEventListener('change', apply);
    apply();
  }

  // ---- Шаг 3: предпросмотр сроков ----
  const short = (iso) => (iso ? iso.slice(8, 10) + '.' + iso.slice(5, 7) : '');
  $$('[data-preview]').forEach((input) => input.addEventListener('input', () => {
    const p = input.dataset.preview;
    const a = $('#' + p + '_start').value, b = $('#' + p + '_end').value;
    const out = $('[data-preview-out="' + p + '"]');
    const fs = input.closest('[data-range]');
    const empty = !a || !b, bad = !empty && b < a;
    if (out) out.textContent = empty ? 'не объявлено' : short(a) + '–' + short(b);
    if (fs) {
      const chip = $('[data-range-chip]', fs), note = $('[data-range-note]', fs);
      chip.textContent = empty ? 'Не указан' : (bad ? 'Ошибка' : 'Указан');
      chip.className = 'pill ' + (empty ? 'warn' : (bad ? 'bad' : 'ok'));
      fs.style.borderColor = empty ? '#F3D9A6' : (bad ? '#E9A99E' : 'transparent');
      note.style.display = empty || bad ? '' : 'none';
      note.textContent = bad ? 'Дата окончания раньше даты начала.' : 'Укажите обе даты, иначе студенты не увидят этот срок в приложении.';
      note.style.color = bad ? '#8C2A1C' : '';
    }
  }));
  const titleInput = $('#title'), titleOut = $('[data-preview-title]');
  if (titleInput && titleOut) titleInput.addEventListener('input', () => { titleOut.textContent = (titleInput.value.trim() || 'Практика').toUpperCase(); });

  // ---- Рапорт ----
  const root = $('#report');
  if (root) initReport(root);

  function initReport(root) {
    const people = JSON.parse(root.dataset.students);
    const groups = JSON.parse(root.dataset.groups);
    const leadOf = {}; groups.forEach((g) => { leadOf[g.title] = g.lead; });
    const leads = Array.from(new Set(groups.map((g) => g.lead).filter(Boolean)));
    const S = { mode: 'leads', selG: new Set(), selL: new Set(), excluded: new Set(), extra: new Set(), edits: {}, onlyConfirmed: true, adding: false, q: '' };
    const docDirty = {};
    const esc = (s) => String(s == null ? '' : s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
    const val = (p, k) => (S.edits[p.id] && S.edits[p.id][k] !== undefined ? S.edits[p.id][k] : p[k]);
    const included = (p) => {
      if (S.excluded.has(p.id)) return false;
      if (S.extra.has(p.id)) return true;
      if (S.onlyConfirmed && !p.has_place) return false;
      return S.mode === 'groups' ? S.selG.has(p.group) : S.selL.has(p.lead);
    };
    const cols = 'grid-template-columns: minmax(200px, 2fr) minmax(140px, 1fr) minmax(160px, 2fr) minmax(130px, 1.4fr) 44px';

    function render() {
      $$('[data-mode]', root).forEach((b) => b.setAttribute('aria-selected', String(b.dataset.mode === S.mode)));
      const src = S.mode === 'groups'
        ? groups.map((g) => ({ key: g.title, label: g.title, hint: '', on: S.selG.has(g.title) }))
        : leads.map((l) => ({ key: l, label: l, hint: groups.filter((g) => g.lead === l).map((g) => g.title).join(', '), on: S.selL.has(l) }));
      $('[data-sources]', root).innerHTML = src.length ? src.map((o) =>
        '<button type="button" class="chip lg" aria-pressed="' + o.on + '" data-src="' + esc(o.key) + '"><b aria-hidden="true">' + (o.on ? '✓' : '+') + '</b>' + esc(o.label) +
        (o.hint ? ' <small>' + esc(o.hint) + '</small>' : '') + '</button>').join('')
        : '<span class="muted">' + (S.mode === 'groups' ? 'Групп нет' : 'Руководители не назначены — укажите их на шаге 2') + '</span>';

      const inList = people.filter(included);
      $('[data-rows]', root).innerHTML = inList.map((p) =>
        '<div class="tr" style="' + cols + '" data-id="' + p.id + '">' +
        '<input class="cell-input" style="font-weight:500" data-k="name" aria-label="ФИО" value="' + esc(val(p, 'name')) + '">' +
        '<input class="cell-input" data-k="group" aria-label="Группа" value="' + esc(val(p, 'group')) + '">' +
        '<input class="cell-input" data-k="place" aria-label="Место практики" placeholder="не выбрано" value="' + esc(val(p, 'place')) + '"' + (val(p, 'place') ? '' : ' style="color:#8A4B00"') + '>' +
        '<span style="font-size:14px; color:var(--ink-2)">' + esc(p.lead || '—') + '</span>' +
        '<button type="button" class="icon-btn" data-remove aria-label="Убрать из рапорта: ' + esc(val(p, 'name')) + '"><svg aria-hidden="true" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg></button>' +
        '</div>').join('');
      $('[data-empty]', root).hidden = inList.length > 0;
      $$('[data-count]', root).forEach((el) => { el.textContent = inList.length; });

      const panel = $('[data-add-panel]', root);
      panel.hidden = !S.adding;
      $('[data-toggle-add]', root).textContent = S.adding ? 'Готово' : '+ Добавить студента';
      if (S.adding) {
        const q = S.q.toLowerCase();
        const cands = people.filter((p) => !included(p) && (!q || p.name.toLowerCase().indexOf(q) >= 0 || p.group.toLowerCase().indexOf(q) >= 0));
        $('[data-candidates]', root).innerHTML = cands.length
          ? cands.slice(0, 80).map((p) => '<button type="button" class="chip" data-add="' + p.id + '">+ ' + esc(p.name) + ' <small>· ' + esc(p.group) + '</small></button>').join('') +
            (cands.length > 80 ? '<span class="muted" style="font-size:13px; align-self:center">и ещё ' + (cands.length - 80) + ' — уточните поиск</span>' : '')
          : '<span class="muted" style="font-size:13px">Все студенты уже в рапорте</span>';
      }

      // Группы и руководители — из выбранного в «Кого включить» плюс из студентов в рапорте
      const selGroups = S.mode === 'groups'
        ? groups.filter((g) => S.selG.has(g.title)).map((g) => g.title)
        : groups.filter((g) => S.selL.has(g.lead)).map((g) => g.title);
      const usedGroups = Array.from(new Set(selGroups.concat(inList.map((p) => val(p, 'group'))).filter(Boolean)));
      const usedLeads = Array.from(new Set(usedGroups.map((t) => leadOf[t])
        .concat(S.mode === 'leads' ? Array.from(S.selL) : [], inList.map((p) => p.lead)).filter(Boolean)));
      if (!docDirty.group) $('[data-doc="group"]', root).value = usedGroups.join(', ');
      if (!docDirty.head_teacher) $('[data-doc="head_teacher"]', root).value = usedLeads.join(', ');
    }

    root.addEventListener('click', (e) => {
      const b = e.target.closest('button'); if (!b) return;
      if (b.dataset.mode) { S.mode = b.dataset.mode; render(); }
      else if (b.dataset.src !== undefined) {
        const set = S.mode === 'groups' ? S.selG : S.selL;
        set.has(b.dataset.src) ? set.delete(b.dataset.src) : set.add(b.dataset.src);
        render();
      } else if (b.hasAttribute('data-remove')) {
        const id = Number(b.closest('[data-id]').dataset.id);
        S.excluded.add(id); S.extra.delete(id); render();
      } else if (b.dataset.add) {
        const id = Number(b.dataset.add);
        S.extra.add(id); S.excluded.delete(id); render();
      } else if (b.hasAttribute('data-toggle-add')) { S.adding = !S.adding; render(); }
      else if (b.hasAttribute('data-download')) download(b);
    });
    root.addEventListener('input', (e) => {
      const t = e.target;
      if (t.dataset.k) {
        const id = Number(t.closest('[data-id]').dataset.id);
        S.edits[id] = Object.assign({}, S.edits[id], { [t.dataset.k]: t.value });
        if (t.dataset.k === 'place') t.style.color = t.value ? '' : '#8A4B00';
      } else if (t.dataset.doc) {
        // Очистили поле вручную — снова подставляем автоматически
        docDirty[t.dataset.doc] = t.value.trim() !== '';
        if (!docDirty[t.dataset.doc]) render();
      }
      else if (t.matches('[data-cand-search]')) { S.q = t.value; render(); t.focus(); }
    });
    root.addEventListener('change', (e) => {
      if (e.target.matches('[data-only-confirmed]')) { S.onlyConfirmed = e.target.checked; render(); }
      if (e.target.dataset.k === 'group') render();
    });

    function download(btn) {
      const rows = people.filter(included).map((p) => ({ name: val(p, 'name'), place: val(p, 'place') }));
      if (!rows.length) { alertMsg('Добавьте в рапорт хотя бы одного студента'); return; }
      const body = { rows };
      $$('[data-doc]', root).forEach((i) => { body[i.dataset.doc] = i.value; });
      const label = btn.textContent; btn.disabled = true; btn.textContent = 'Формируем…';
      fetch(btn.dataset.url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) })
        .then((r) => {
          if (!r.ok) return r.json().then((j) => { throw new Error(j.message || 'Ошибка'); });
          const cd = r.headers.get('Content-Disposition') || '';
          const m = cd.match(/filename\*=UTF-8''([^;]+)/i) || cd.match(/filename="?([^";]+)"?/i);
          return r.blob().then((blob) => ({ blob, name: m ? decodeURIComponent(m[1]) : 'Рапорт.docx' }));
        })
        .then(({ blob, name }) => {
          const a = document.createElement('a'); a.href = URL.createObjectURL(blob); a.download = name;
          document.body.appendChild(a); a.click(); setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 1000);
        })
        .catch((err) => alertMsg(err.message))
        .finally(() => { btn.disabled = false; btn.textContent = label; });
    }
    function alertMsg(text) {
      let box = $('[data-report-msg]', root);
      if (!box) { box = document.createElement('div'); box.className = 'alert alert-danger'; box.setAttribute('data-report-msg', ''); box.setAttribute('role', 'alert'); $('aside .hero', root).appendChild(box); }
      box.textContent = text;
    }
    render();
  }
})();
