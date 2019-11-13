const bindFlashClose = () => {
  const closeBtn = document.querySelector('.flash-close')

  if (typeof(closeBtn) != 'undefined' && closeBtn != null) {
    closeBtn.addEventListener('click', (e) => {
      const target = e.target
      target.parentNode.remove()
    })
  }
}

const bindMovieDelete = () => {
  const deleteBtns = document.querySelectorAll('.btn-delete')
  for (const deleteBtn of deleteBtns) {
    deleteBtn.addEventListener('click', e => {
      const target = e.target
      const movieItem = target.parentNode.parentNode
      const movieID = movieItem.dataset.movieId
      fetch(`/api/v1/movie/${movieID}`, {
        method: 'DELETE',
      }).then(res => res.json())
      .then(data => window.location.reload())
      .catch(err => console.log(err))
    })
  }
}

const bindMovieEditCancel = () => {
  const editCancelBen = document.querySelector('.btn-edit-cancel')
  editCancelBen.addEventListener('click', e => {
    const target = e.target
    const movieItem = target.parentNode.parentNode
    const year = movieItem.querySelector('input[name=year]').value
    const title = movieItem.querySelector('input[name=title]').value
    movieItem.innerHTML = `
      <span>
        ${title} - ${year}
      </span>
      <span class="float-right">
        <button class="btn btn-info btn-edit">Edit</button>
        <button class="btn btn-danger btn-delete">Delete</button>
        <span>|</span>
        <a class="douban" href="https://movie.douban.com/subject_search?search_text=${title}"
           target="_blank" title="Find this movie on IMDb">douban</a>
        <a class="imdb" href="https://www.imdb.com/find?q=${title}" target="_blank"
           title="Find this movie on IMDb">IMDb</a>
      </span>
    `
    // 重新绑定更新操作
    bindMovieEdit()
    // 重新绑定删除操作
    bindMovieDelete()
  })
}

const bindMovieEditUpdate = () => {
  const editCancelBtn = document.querySelector('.btn-edit-update')
  editCancelBtn.addEventListener('click', e => {
    const target = e.target
    const movieItem = target.parentNode.parentNode
    const movieID = movieItem.dataset.movieId
    const year = movieItem.querySelector('input[name=year]').value
    const title = movieItem.querySelector('input[name=title]').value

    fetch(`/api/v1/movie/${movieID}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        year,
        title
      })
    }).then(res => res.json())
    .then(data => window.location.reload())
    .catch(err => console.log(err))
  })
}

const editAction = (e) => {
  const target = e.target
  const movieItem = target.parentNode.parentNode
  const movieItemContent = movieItem.innerHTML
  const movieDetail = movieItem.children[0].innerHTML
  const [title, year] = movieDetail.trim().split(' - ')

  movieItem.innerHTML = `
    <span>
      <input type="text" name="title" value=${title} />
      <input type="text" name="year" value=${year} maxlength="4" size="4" />
    </span>
    <span class="float-right">
      <button class="btn btn-primary btn-edit-update">Update</button>
      <button class="btn btn-edit-cancel">Cancel</button>
    </span>
  `

  bindMovieEditUpdate()
  bindMovieEditCancel()
}

const bindMovieEdit = () => {
  const editBtns = document.querySelectorAll('.btn-edit')
  for (const editBtn of editBtns) {
    editBtn.addEventListener('click', editAction)
  }
}

const main = () => {
  bindFlashClose()
  bindMovieDelete()
  bindMovieEdit()
}

main()