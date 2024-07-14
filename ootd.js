async function fetchAnalysisResult() {
    const response = await fetch('http://localhost:5000/analysis-result');
    const data = await response.json();
    console.log(data);
    return data;
  }
  async function OoTD(){
      let result= await fetchAnalysisResult();
      document.querySelector('#result').innerHTML=`<h3>The most Browsed Dress: ${result.most_browsed_dress}</h3>`;
      const image=`<img src="ootd.png" alt="Outfit of the Day" class="outfit-image" width="400px">`;
      document.querySelector('#image_result').innerHTML=image;
  }
OoTD();

const commentList = document.getElementById('comment-list');
const commentInput = document.getElementById('comment-input');
const postCommentButton = document.getElementById('post-comment');

postCommentButton.addEventListener('click', (e) => {
    e.preventDefault(); // prevent form submission

    const newComment = commentInput.value.trim();
    if (newComment !== '') {
        const newCommentHTML = `
            <li>
                <p>${newComment}</p>
            </li>
        `;
        commentList.innerHTML += newCommentHTML;
        commentInput.value = ''; // clear the input field
    }
});

