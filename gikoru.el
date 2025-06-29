;;; gikoru.el --- Simple static blog generator -*- lexical-binding: t -*-

;; directories ;;

(defconst gikoru-base-dir "./")
(defconst gikoru-merge-dir (expand-file-name "merge" gikoru-base-dir))
(defconst gikoru-pg-dir (expand-file-name "pg" gikoru-base-dir))
(defconst gikoru-posts-dir (expand-file-name "posts" gikoru-base-dir))
(defconst gikoru-static-dir (expand-file-name "static" gikoru-base-dir))
(defconst gikoru-output-dir (expand-file-name "public" gikoru-base-dir))
(defconst gikoru-output-posts-dir (expand-file-name "posts" gikoru-output-dir))
(defconst gikoru-output-sections-dir (expand-file-name "sections" gikoru-output-dir))
(defconst gikoru-output-archive-dir (expand-file-name "archive" gikoru-output-dir))
(defconst gikoru-atom-feed-file (expand-file-name "index.atom" gikoru-output-dir))

;; mutables ;;

(defvar gikoru-post-header-format
                          "<p><small><time datetime=\"%s\">%s</time></small><br>\n
                          <strong><u>%s</u></strong></p>\n")

(defvar gikoru-time-format "%Y-%m-%d :: %H:%M [UTC %z]")

(defvar gikoru-export-posts-header "#+BEGIN_EXPORT html\n%s#+END_EXPORT\n\n%s")

(defvar gikoru-post-html-wrapper-tag "main") ;; change to body if preferred.

(defvar gikoru-index-title "index")

(defvar gikoru-index-title-style
  "#+BEGIN_EXPORT html\n<p>> <strong><u>%s (%d)</u></strong></p>\n#+END_EXPORT")

(defvar gikoru-sections-title
  "#+BEGIN_EXPORT html\n<p>> <strong><u>Sections</u></strong></p>\n#+END_EXPORT")

(defvar gikoru-section-name-title
  (lambda (section)
    (format "#+BEGIN_EXPORT html\n<p>> <strong><u>%s</u></strong></p>\n#+END_EXPORT" section)))


(defvar gikoru-posts-per-page 10)

(defvar gikoru-list-style "#+BEGIN_EXPORT html\n
                           <p><small>%s</small><br><a href=\"%s\">%s</a></p>
                           \n#+END_EXPORT")

(defvar gikoru-section-list-style "#+BEGIN_EXPORT html\n
                                   <p><a href=\"./%s/index.html\">%s</a> (%d article%s)</p>
                                   \n#+END_EXPORT")


(defvar gikoru-archive-toc-entry-format
  "#+BEGIN_EXPORT html\n<p><a href=\"#%s\">%s</a> (%d article%s)</p>\n#+END_EXPORT\n")

(defvar gikoru-archive-section-header-format
  "#+BEGIN_EXPORT html\n<p>* <strong id=\"%s\"><u>%s</u></strong></p>\n#+END_EXPORT\n")

(defvar gikoru-archive-post-format
  "#+BEGIN_EXPORT html\n<p><small>%s</small><br><a href=\"%s\">%s</a></p>\n#+END_EXPORT\n")

(defvar gikoru-archive-toc-header
  "#+BEGIN_EXPORT html\n<p>> <strong><u>Archive</u></strong></p>\n#+END_EXPORT\n")

(defvar gikoru-archive-toc-divider
  "#+BEGIN_EXPORT html\n<hr>\n#+END_EXPORT\n")

(defvar gikoru-archive-section-divider
  "#+BEGIN_EXPORT html\n<br><hr><br>\n#+END_EXPORT\n")

;;;;;;;;;;;;;;

(defun gikoru--read-file (file)
  (with-temp-buffer
    (insert-file-contents file)
    (buffer-string)))

(defun gikoru--merge-org-content (body-content)
  (concat
   (gikoru--read-file (expand-file-name "head.org" gikoru-merge-dir)) "\n"
   (gikoru--read-file (expand-file-name "header.org" gikoru-merge-dir)) "\n"
   body-content "\n"
   (gikoru--read-file (expand-file-name "footer.org" gikoru-merge-dir))))

(defun gikoru--export-posts ()
  "Export all public Org posts from `gikoru-posts-dir` to HTML in `gikoru-output-posts-dir`."
  (unless (file-directory-p gikoru-output-posts-dir)
    (make-directory gikoru-output-posts-dir t))
  (dolist (orgfile (directory-files gikoru-posts-dir t "\\.org$"))
    (let* ((meta (gikoru--extract-post-meta orgfile)))
      (when meta ;; Only if PUBLIC: yes
        (let* ((title (plist-get meta :title))
               (time (plist-get meta :time))
               (section (or (plist-get meta :section) "Null"))
               (section-link (format "<p>:: <a href=\"/sections/%s\">%s</a></p>\n"
                                     (gikoru--sanitize-section-name section)
                                     section))
               (header-html (gikoru--format-post-header title time))
               (raw-body (gikoru--read-file orgfile))
               (wrapped-body (concat
                              (format "#+BEGIN_EXPORT html\n<%s>\n#+END_EXPORT\n"
                                      gikoru-post-html-wrapper-tag)
                              raw-body
                              (format "\n#+BEGIN_EXPORT html\n</%s>\n%s#+END_EXPORT\n"
                                      gikoru-post-html-wrapper-tag section-link)))
               (enhanced-body (format gikoru-export-posts-header header-html wrapped-body))
               (merged-content (gikoru--merge-org-content enhanced-body))
               (basename (file-name-base orgfile))
               (merged-path (expand-file-name (concat basename "-merged.org") gikoru-output-posts-dir))
               (html-path (expand-file-name (concat basename ".html") gikoru-output-posts-dir)))
          ;; Write merged org file
          (with-temp-file merged-path
            (insert merged-content))
          ;; Export to HTML
          (with-current-buffer (find-file-noselect merged-path)
            (org-html-export-to-html nil nil nil t)
            (let ((exported-html (concat (file-name-sans-extension merged-path) ".html")))
              (rename-file exported-html html-path t))
            (kill-buffer))
          ;; Delete merged org file
          (delete-file merged-path)
          (message "Exported %s" html-path))))))

(defun gikoru--extract-post-meta (file)
  (with-temp-buffer
    (insert-file-contents file)
    (let ((title (when (re-search-forward "^#\\+POST-TITLE:[ \t]*\\(.*\\)$" nil t)
                   (match-string 1)))
          (time (when (re-search-forward "^#\\+TIME:[ \t]*\\(.*\\)$" nil t)
                  (match-string 1)))
          (section (when (re-search-forward "^#\\+SECTION:[ \t]*\\(.*\\)$" nil t)
                     (match-string 1)))
          (public (when (re-search-forward "^#\\+PUBLIC:[ \t]*\\(.*\\)$" nil t)
                    (let ((val (match-string 1)))
                      (and val (string= (upcase (string-trim val)) "YES"))))))
      (when (and title time public)
        (list :title title :time time :section section :file file :public public)))))

(defun gikoru--format-post-header (title time)
  (let ((formatted-time (gikoru--format-readable-time time)))
    (format gikoru-post-header-format
            (or time "")
            formatted-time
            (or title "Untitled"))))

(defun gikoru--format-readable-time (iso-time)
  (let ((parsed (ignore-errors (parse-iso8601-time-string iso-time))))
    (if parsed
        (let ((raw (format-time-string gikoru-time-format parsed)))
          ;; Insert colon in timezone offset, e.g. -0400 → -04:00
          (replace-regexp-in-string
           "\\(UTC [+-][0-9]\\{2\\}\\)\\([0-9]\\{2\\}\\)"
           "\\1:\\2"
           raw))
      iso-time)))

(defun gikoru--time-to-date (time-str)
  (when (and time-str (string-match "\\([0-9]\\{4\\}-[0-9]\\{2\\}-[0-9]\\{2\\}\\)" time-str))
    (match-string 1 time-str)))

(defun gikoru--sanitize-section-name (section)
  (replace-regexp-in-string "[^a-zA-Z0-9_-]" "-" (downcase section)))

(defun gikoru--export-sections ()
  (let* ((files (directory-files gikoru-posts-dir t "\\.org$"))
         (posts-meta (delq nil (mapcar #'gikoru--extract-post-meta files)))
         (section-hash (make-hash-table :test 'equal)))
    
    ;; do group by post
    (dolist (meta posts-meta)
      (let* ((section (or (plist-get meta :section) "Null"))
             (list (gethash section section-hash)))
        (puthash section (cons meta list) section-hash)))

    ;; create dir in case
    (unless (file-directory-p gikoru-output-sections-dir)
      (make-directory gikoru-output-sections-dir t))

    (maphash
     (lambda (section posts)
       (let* ((safe-name (gikoru--sanitize-section-name section))
              (section-dir (expand-file-name safe-name gikoru-output-sections-dir))
              (section-org (expand-file-name "index-temp.org" section-dir))
              (section-html (expand-file-name "index.html" section-dir))
              (merged-content
               (gikoru--merge-org-content
                (concat
                 (funcall gikoru-section-name-title section) "\n\n"
                 (mapconcat
                  (lambda (post)
                    (let* ((title (plist-get post :title))
                           (time (plist-get post :time))
                           (date (gikoru--time-to-date time))
                           (file (plist-get post :file))
                           (html-name (concat (file-name-base file) ".html"))
                           (link (format "/posts/%s" html-name)))
                      (format gikoru-list-style
                              date link title)))
                  (sort posts
                        (lambda (a b)
                          (string> (plist-get a :time) (plist-get b :time))))
                  "\n")))))
         (unless (file-directory-p section-dir)
           (make-directory section-dir t))
         (with-temp-file section-org
           (insert merged-content))
         (with-current-buffer (find-file-noselect section-org)
           (org-html-export-to-html nil nil nil t)
           (let ((exported-html (concat (file-name-sans-extension section-org) ".html")))
             (rename-file exported-html section-html t))
           (kill-buffer))
         (delete-file section-org)))
     section-hash)

    ;; sort hash
    (let* ((alist (let (acc)
                    (maphash (lambda (k v) (push (cons k v) acc)) section-hash)
                    acc))
           ;; case-insensitve
           (sorted-alist (sort alist (lambda (a b)
                                       (string-lessp
                                        (downcase (car a))
                                        (downcase (car b))))))
           (sections-index-org (expand-file-name "index-temp.org" gikoru-output-sections-dir))
           (sections-index-html (expand-file-name "index.html" gikoru-output-sections-dir))
           (body-content
            (concat
             gikoru-sections-title "\n\n"
             (mapconcat
              (lambda (pair)
                (let* ((section (car pair))
                       (posts (cdr pair))
                       (safe-name (gikoru--sanitize-section-name section))
                       (count (length posts)))
                  (format gikoru-section-list-style
                          safe-name section count (if (= count 1) "" "s"))))
              sorted-alist
              "\n")))
           (merged-content (gikoru--merge-org-content body-content)))
      (with-temp-file sections-index-org
        (insert merged-content))
      (with-current-buffer (find-file-noselect sections-index-org)
        (org-html-export-to-html nil nil nil t)
        (let ((exported-html (concat (file-name-sans-extension sections-index-org) ".html")))
          (rename-file exported-html sections-index-html t))
        (kill-buffer))
      (delete-file sections-index-org))))

(defun gikoru--generate-post-list-org ()
  (let* ((posts-dir (expand-file-name "posts" gikoru-base-dir))
         (files (directory-files posts-dir t "\\.org$"))
         (posts-meta
          (delq nil
                (mapcar #'gikoru--extract-post-meta files)))
         (sorted (sort posts-meta
                       (lambda (a b)
                         (string> (plist-get a :time) (plist-get b :time)))))
         (content (concat "_" gikoru-index-title "_\n\n")))
    (dolist (post sorted)
      (let* ((title (plist-get post :title))
             (time (plist-get post :time))
             (date (gikoru--time-to-date time)) ;; YYYY-MM-DD
             (file (plist-get post :file))
             (html-name (concat (file-name-base file) ".html"))
             (link (format "/posts/%s" html-name)))
	(setq content
              (concat content
                      (format gikoru-list-style
                              date link title)))))
    content))

(defun gikoru--render-pagination (current-page total-pages base-url &optional max-pages-visible)
  (if (= total-pages 1)
      ""  ;; No pagination needed
    (let* ((max-pages-visible (or max-pages-visible 5))
           (block-start 1)
           (block-end total-pages)
           (html ""))
      (if (<= total-pages max-pages-visible)
          (setq block-start 1 block-end total-pages)
        (cond
         ((<= current-page 3)
          (setq block-start 1 block-end max-pages-visible))
         ((>= current-page (- total-pages 2))
          (setq block-start (- total-pages (1- max-pages-visible))
                block-end total-pages))
         (t
          (setq block-start (- current-page 2)
                block-end (+ current-page 2)))))
      (when (< block-start 1) (setq block-start 1))
      ;; Previous arrows
      (when (> current-page 1)
        (setq html (concat html
                           (format "<a href=\"index.html\">&laquo;</a> ")))
        (setq html (concat html
                           (format "<a href=\"%s\">&lsaquo;</a> "
                                   (if (= current-page 2) "index.html"
                                     (format "%s%d.html" base-url (1- current-page)))))))
      ;; Page numbers
      (dotimes (i (- block-end block-start -1))
        (let* ((p (+ block-start i))
               (url (if (= p 1) "index.html" (format "%s%d.html" base-url p))))
          (if (= p current-page)
              (setq html (concat html (format " %02d " p)))
            (setq html (concat html (format "<a href=\"%s\">%02d</a> " url p))))))
      ;; Next arrows
      (when (< current-page total-pages)
        (setq html (concat html
                           (format "<a href=\"%s\">&rsaquo;</a> "
                                   (format "%s%d.html" base-url (1+ current-page)))))
        (setq html (concat html
                           (format "<a href=\"%s\">&raquo;</a>"
                                   (format "%s%d.html" base-url total-pages)))))
      ;; Wrap in left-aligned div
      (format "<div class=\"pagination\">\n%s\n</div>\n" html))))

(defun gikoru--export-index (&optional posts-per-page)
  (let* ((posts-per-page (or posts-per-page 10))
         (posts-dir (expand-file-name "posts" gikoru-base-dir))
         (files (directory-files posts-dir t "\\.org$"))
         (posts-meta (delq nil (mapcar #'gikoru--extract-post-meta files)))
         (sorted (sort posts-meta (lambda (a b)
                                    (string> (plist-get a :time)
                                             (plist-get b :time)))))
         (total-posts (length sorted))
         (total-pages (max 1 (ceiling (/ (float total-posts) posts-per-page)))))

    ;; paginate
    (dotimes (page total-pages)
      (let* ((start (* page posts-per-page))
             (end (min total-posts (+ start posts-per-page)))
             (page-posts (cl-subseq sorted start end))
             (page-number (1+ page))
             (file-name (if (= page-number 1)
                            "index-temp.org"
                          (format "pg%d-temp.org" page-number)))
             (html-name (if (= page-number 1)
                            "index.html"
                          (format "pg%d.html" page-number)))
             (org-path (expand-file-name file-name gikoru-output-dir))
             (html-path (expand-file-name html-name gikoru-output-dir))
             (body-content
              (concat
               (format gikoru-index-title-style gikoru-index-title page-number total-pages)
               "\n\n"
               (mapconcat
                (lambda (post)
                  (let* ((title (plist-get post :title))
                         (time (plist-get post :time))
                         (date (gikoru--time-to-date time))
                         (file (plist-get post :file))
                         (html-name (concat (file-name-base file) ".html"))
                         (link (format "/posts/%s" html-name)))
                    (format gikoru-list-style date link title)))
                page-posts "\n"))))

        (setq body-content
              (concat body-content
                      "\n#+BEGIN_EXPORT html\n"
                      (gikoru--render-pagination page-number total-pages "pg")
                      "#+END_EXPORT\n"))

        ;; Merge and write org and html files
        (let ((merged (gikoru--merge-org-content body-content)))
          (with-temp-file org-path (insert merged))
          (with-current-buffer (find-file-noselect org-path)
            (org-html-export-to-html nil nil nil t)
            (let ((exported-html (concat (file-name-sans-extension org-path) ".html")))
              (rename-file exported-html html-path t))
            (kill-buffer))
          (delete-file org-path))))
    
    (message "Blog index exported (total %d pages)" total-pages)))

(defun gikoru--export-static ()
  (when (file-directory-p gikoru-static-dir)
    (let ((files (directory-files-recursively gikoru-static-dir ".*")))
      (dolist (src files)
        (let* ((rel (file-relative-name src gikoru-static-dir))
               (dest (expand-file-name rel gikoru-output-dir)))
          (cond
           
           ((string-suffix-p ".org" src t)
            (let ((html-dest (concat (file-name-sans-extension dest) ".html")))
              (with-current-buffer (find-file-noselect src)
                (org-html-export-to-html nil nil nil t)
                (rename-file (concat (file-name-sans-extension src) ".html")
                             html-dest t)
                (kill-buffer))))
           
           ((file-directory-p src)
            (make-directory dest t))
           
           (t
            (make-directory (file-name-directory dest) t)
            (copy-file src dest t))))))))


(defun gikoru--export-archive ()
  (let ((gikoru-output-archive-dir (expand-file-name "archive" gikoru-output-dir)))
    (unless (file-directory-p gikoru-output-archive-dir)
      (make-directory gikoru-output-archive-dir t))

    (let* ((files (directory-files gikoru-posts-dir t "\\.org$"))
           (posts-meta (delq nil (mapcar #'gikoru--extract-post-meta files)))
           (public-posts (cl-remove-if-not (lambda (meta) (plist-get meta :public)) posts-meta))
           (grouped (make-hash-table :test 'equal)))

      
      (dolist (meta public-posts)
        (let ((time (plist-get meta :time)))
          (when (and time (>= (length time) 7))
            (let ((ym (substring time 0 7))) ;; "YYYY-MM"
              (puthash ym (cons meta (gethash ym grouped)) grouped)))))

      (let* ((year-months (sort (hash-table-keys grouped) #'string>))
             (toc
              (concat gikoru-archive-toc-header
                      (mapconcat
                       (lambda (ym)
                         (let* ((anchor-id (replace-regexp-in-string "-" "_" ym))
                                (posts (gethash ym grouped))
                                (count (length posts)))
                           (format gikoru-archive-toc-entry-format
                                   anchor-id ym count (if (= count 1) "" "s"))))
                       year-months
                       "")
                      gikoru-archive-toc-divider))
             (sections
              (mapconcat
               (lambda (ym)
                 (let* ((anchor-id (replace-regexp-in-string "-" "_" ym))
                        (posts (sort (gethash ym grouped)
                                     (lambda (a b)
                                       (string> (plist-get a :time)
                                                (plist-get b :time)))))
                        (header (format gikoru-archive-section-header-format anchor-id ym))
                        (post-lines
                         (mapconcat
                          (lambda (post)
                            (let* ((title (plist-get post :title))
                                   (time (plist-get post :time))
                                   (date (if (and time (>= (length time) 10))
                                             (substring time 8 10)
                                           ""))
                                   (file (plist-get post :file))
                                   (html-name (concat (file-name-base file) ".html"))
                                   (link (format "/posts/%s" html-name)))
                              (format gikoru-archive-post-format date link title)))
                          posts "\n")))
                   (concat header "\n" post-lines "\n" gikoru-archive-section-divider)))
               year-months "\n\n"))

             (full-body (concat "#+TITLE: Archive\n\n" toc "\n\n" sections))
             (org-file (expand-file-name "index-temp.org" gikoru-output-archive-dir))
             (html-file (expand-file-name "index.html" gikoru-output-archive-dir))
             (merged (gikoru--merge-org-content full-body)))

        
        (with-temp-file org-file (insert merged))
        (with-current-buffer (find-file-noselect org-file)
          (org-html-export-to-html nil nil nil t)
          (let ((exported-html (concat (file-name-sans-extension org-file) ".html")))
            (rename-file exported-html html-file t))
          (kill-buffer))
        (delete-file org-file)
        (message "Archive page exported to %s" html-file)))))

(defun gikoru--export-pg ()
  (let ((org-files (directory-files gikoru-pg-dir t "\\.org$")))
    (dolist (file org-files)
      (let* ((content (gikoru--read-file file))
             (merged (gikoru--merge-org-content content))
             (basename (file-name-base file))
             (temp-org-path (expand-file-name (concat basename "-temp.org") gikoru-output-dir))
             (html-path (expand-file-name (concat basename ".html") gikoru-output-dir)))
        
        (with-temp-file temp-org-path
          (insert merged))
        ;; Export to HTML
        (with-current-buffer (find-file-noselect temp-org-path)
          (org-html-export-to-html nil nil nil t)
          (let ((exported-html (concat (file-name-sans-extension temp-org-path) ".html")))
            (rename-file exported-html html-path t))
          (kill-buffer))
        ;; Clean up temp file
        (delete-file temp-org-path)
        (message "Exported: %s" html-path)))))

;; atom

(defun gikoru--read-org-body (file)
  (with-temp-buffer
    (insert-file-contents file)
    (goto-char (point-min))
    (forward-line 4) ;; skip metadata lines
    (let* ((content (buffer-substring-no-properties (point) (point-max)))
           (cleaned (replace-regexp-in-string
                     "^#\\+BEGIN_EXPORT.*\n\\|^#\\+END_EXPORT.*\n"
                     ""
                     content t t)))
      (string-trim cleaned)))) ;; trim whitespace at start/end

(defun gikoru--xml-escape (string)
  (xml-escape-string string))

(defun gikoru--generate-atom-feed (input-dir output-file feed-meta)
  (let ((xml-ns "http://www.w3.org/2005/Atom")
        (entries '()))
    ;; Collect entries from .org files in INPUT-DIR
    (dolist (file (directory-files input-dir t "\\.org$"))
      (let ((meta (gikoru--extract-post-meta file)))
        (when meta
          (let* ((title (plist-get meta :title))
                 (time (plist-get meta :time))
                 (entry-id (format "%s%s" (plist-get feed-meta :id)
                                   (file-name-nondirectory file)))
                 (escaped-title (gikoru--xml-escape title))
                 (html-content
                  (with-current-buffer (find-file-noselect file)
                    (goto-char (point-min))
                    (forward-line 4) ;; skip metadata
                    (let ((org-export-with-toc nil)
                          (org-export-with-section-numbers nil))
                      (prog1
                          (org-export-as 'html nil nil t nil)
                        (kill-buffer)))))
                 (published-time (format-time-string
                                  "%Y-%m-%dT%H:%M:%S%:z"
                                  (date-to-time time))))
            (push (list :title escaped-title
                        :id entry-id
                        :link (format "%sposts/%s.html"
                                      (plist-get feed-meta :id)
                                      (file-name-base file))
                        :published published-time
                        :updated published-time
                        :content html-content)
                  entries)))))
    ;; Sort entries newest first
    (setq entries (cl-sort entries
                           (lambda (a b)
                             (string> (plist-get a :published)
                                      (plist-get b :published)))))
    ;; Write the Atom feed XML
    (with-temp-buffer
      (insert "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n")
      (insert (format "<feed xmlns=\"%s\">\n" xml-ns))
      ;; Insert feed metadata tags
      (dolist (tag '(:id :title :updated :generator))
        (when-let ((val (plist-get feed-meta tag)))
          (insert (format "<%s>%s</%s>\n"
                          (substring (symbol-name tag) 1)
                          (gikoru--xml-escape val)
                          (substring (symbol-name tag) 1)))))
      ;; Insert author info
      (when (plist-get feed-meta :author)
        (insert "<author>\n")
        (insert (format "  <name>%s</name>\n"
                        (gikoru--xml-escape (plist-get feed-meta :author))))
        (when (plist-get feed-meta :author_uri)
          (insert (format "  <uri>%s</uri>\n"
                          (gikoru--xml-escape (plist-get feed-meta :author_uri)))))
        (insert "</author>\n"))
      ;; Insert links
      (dolist (link (plist-get feed-meta :links))
        (insert (format "<link rel=\"%s\" href=\"%s\"%s/>\n"
                        (gikoru--xml-escape (plist-get link :rel))
                        (gikoru--xml-escape (plist-get link :href))
                        (if-let ((type (plist-get link :type)))
                            (format " type=\"%s\"" (gikoru--xml-escape type))
                          ""))))
      ;; Insert entries
      (dolist (entry entries)
        (insert "<entry>\n")
        (insert (format "  <id>%s</id>\n" (plist-get entry :id)))
        (insert (format "  <title>%s</title>\n" (plist-get entry :title)))
        (insert (format "  <link href=\"%s\"/>\n" (plist-get entry :link)))
        (insert (format "  <published>%s</published>\n" (plist-get entry :published)))
        (insert (format "  <updated>%s</updated>\n" (plist-get entry :updated)))
        (insert (format "  <content type=\"html\"><![CDATA[%s]]></content>\n"
                        (plist-get entry :content)))
        (insert "</entry>\n"))
      (insert "</feed>\n")
      (write-region (point-min) (point-max) output-file))
    (message "Atom feed written to %s" output-file)))

(defun gikoru ()
  (interactive)
  (let ((feed-meta
         (list :title "akai.gikopoi.com"
               :author "akai"
               :author_uri "https://akai.gikopoi.com/"
               :id "https://akai.gikopoi.com/"
               :updated (format-time-string "%Y-%m-%dT%H:%M:%S%:z" (current-time) t)
               :generator "https://github.com/archmageakai/gikoru"
               :links (list (list :rel "alternate" :href "https://akai.gikopoi.com/")
                            (list :rel "self" :href "https://akai.gikopoi.com/index.atom"
                                  :type "application/atom+xml")))))
    (gikoru--export-posts)
    (gikoru--export-index gikoru-posts-per-page)
    (gikoru--export-sections)
    (gikoru--export-static)
    (gikoru--export-archive)
    (gikoru--export-pg)
    (gikoru--generate-atom-feed gikoru-posts-dir gikoru-atom-feed-file feed-meta)
    (message "Gikoru blog export complete.")))

(provide 'gikoru)

;;; gikoru.el ends here
